from flask import current_app, jsonify, Response, request
from flask_restful import Resource

from app.models.chat_session import ChatSession, Status
from app.models.chat import Chat, CreatedBy
from app.models.user import User
from app.models.product import Product
from app.models.result import Result

from app.middlewares.auth import Auth
from ml.similarity import SimilarityCalculator
from app.utils.common import row2dict, rows2dict
from app.utils.common import map_row
from app.db import db
import re
import locale
from sqlalchemy import cast, Integer

auth = Auth()


def result_row_callback(result, row):
    return result | {
        "createdAt": result["createdAt"].strftime("%Y-%m-%dT%H:%M:%S%z"),
        "updatedAt": result["updatedAt"].strftime("%Y-%m-%dT%H:%M:%S%z"),
        "product": map_row(row.product),
    }


def map_result(result):
    result_dict = row2dict(result, snake_to_camel=True)
    return result_row_callback(result_dict, result) if result_dict else None


def map_results(results):
    return rows2dict(results, snake_to_camel=True, row_callback=result_row_callback)


def extract_number(text):
    numbers = re.findall(r"\d+[\.,]?\d*", text)
    if numbers:
        locale.setlocale(locale.LC_ALL, "")
        return locale.atof(numbers[0])
    else:
        return None


class ResultRatingApi(Resource):
    @auth.middleware
    def post(token_data, self, id, rating):
        result = self.db.session.merge(Result(id=id, user_rating=rating))
        return map_result(result)


class ResultApi(Resource):
    @auth.middleware
    def get(token_data, self, chat_session_id, id):
        result = (
            db.session.query(Result)
            .filter_by(id=id, chat_session_id=chat_session_id)
            .first()
        )

        return map_result(result)


class GenerateResultsApi(Resource):
    @auth.middleware
    def post(token_data, self, chat_session_id):
        chat_session = (
            db.session.query(ChatSession)
            .filter_by(id=chat_session_id, user_id=token_data["userId"])
            .first()
        )

        if not chat_session:
            raise MissingChatSessionError()

        if chat_session.status == Status.complete:
            results = (
                db.session.query(Result)
                .filter(Result.chat_session_id == chat_session_id)
                .all()
            )
            # print(map_results(results))
            return map_results(results)

        # If no results, generate results
        generator = ResultsGenerator(token_data["userId"], chat_session)
        results = generator.generate()
        print(map_results(results))
        return map_results(results)


class ResultsGenerator:
    def __init__(self, user_id, chat_session):
        self.user_id = user_id
        self.chat_session = chat_session

    # key是question.code，value是chat对象
    def get_qna_dict(self, chats):
        r = {}
        for i in range(len(chats)):
            chat = chats[i]
            if (
                chat.created_by == CreatedBy.user
                and chat.question
                and chat.question.code
            ):
                key = chat.question.code

                if key:
                    r[key] = chat
        return r

    def get_context_values(self, chats):
        context_groups = ["context", "style"]
        r = {}
        for i in range(len(chats)):
            chat = chats[i]
            if (
                chat.created_by == CreatedBy.user
                and chat.question
                and chat.question.code
                and chat.question.group in context_groups
            ):
                key = chat.question.code

                if key:
                    weights = chat.question.weights
                    # Handle MCQs
                    if chat.option:
                        for weight in weights:
                            r[weight.variable] = (
                                chat.option.parse_value() * weight.weight_value
                            )
        return r

    # 返回整行result
    def generate(self):
        chats = self.chat_session.chats if self.chat_session else []

        if not chats:
            raise MissingChatSessionError()

        qna = self.get_qna_dict(chats)
        products = rows2dict(Product.query.all(), "id")

        # Get interest text, question.code = 'interest_open',提取出chat的内容
        description_input = qna["general"].message_text if qna["general"] else ""
        taste_exp_input = qna["flavour"].message_text if qna["flavour"] else ""
        variety_input = qna["brand"].message_text if qna["brand"] else ""
        pairing_input = qna["pairing"].message_text if qna["pairing"] else ""

        # Get context values
        context_input = self.get_context_values(chats)

        # Get price text
        price_input = qna["highest_price"].message_text if qna["highest_price"] else ""
        price_input = extract_number(price_input)

        # Calculate similarity score
        calculator = SimilarityCalculator(
            products,
            description_input,
            taste_exp_input,
            variety_input,
            pairing_input,
            price_input,
        )

        recommendations = calculator.get_recommendation()

        # Save recommendations
        for each in Result.query.filter(
            Result.chat_session_id == self.chat_session.id,
            cast(Result.product_id, Integer).in_(recommendations.keys()),
        ).all():
            # Only merge those results which already exist in the database
            update_item = recommendations.pop(each.product_id)
            db.session.merge(
                Result(
                    **update_item,
                    chat_session_id=self.chat_session.id,
                    product_id=each.product_id
                )
            )

        def map_result_values(key):
            value = recommendations[key]
            return Result(**value, chat_session_id=self.chat_session.id, product_id=key)

        # Only add those results which did not exist in the database
        insert_items = list(map(map_result_values, recommendations.keys()))
        db.session.add_all(insert_items)

        # Save session completed state
        self.chat_session.status = Status.complete
        db.session.commit()
        print(db.session.query(Result).filter(Result.chat_session_id == self.chat_session.id).all())
        return (
            db.session.query(Result)
            .filter(Result.chat_session_id == self.chat_session.id)
            .all()
        )


class MissingChatSessionError(Exception):
    """Missing chat session error"""
