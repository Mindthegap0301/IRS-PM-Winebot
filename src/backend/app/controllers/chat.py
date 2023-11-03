from flask import current_app, jsonify, Response, request
from flask_restful import Resource
from sqlalchemy import asc, desc, select, join
import Levenshtein as lev

from app.models.chat import Chat, CreatedBy
from app.models.chat_session import ChatSession, Status
from app.models.question import Question
from app.models.user import User

from app.middlewares.auth import Auth

from app.db import db

import random


auth = Auth()

#get_options_dict()用于将问题options选项转换为字典格式
def get_options_dict(options):
    return list(map(lambda option: {'id': option.id, 'order': option.order, 'value': option.value, 'data_type': option.data_type.name, 'label': option.label}, options)) if options else None

#找到输入文本和options之间的接近option，返回
def get_nearest_option(input, options):
    if options:
        distances = [lev.distance(input, option.label) for option in options]
        min_value = min(distances)
        min_index = distances.index(min_value)
        return options[min_index]

#处理聊天请求，get在数据库中获取特定用户的聊天记录，返回chats列表
#post处理：生成回复和保存

#get: 通过session对象，创建数据库query对查询chat，filter_by筛选出id等于tokenid的，就是根据身份信息进行筛选
class ChatsApi(Resource):
    @auth.middleware
    def get(token_data, self):
        chats = db.session.query(Chat).filter_by(
            user_id=token_data['userId']).all()
        return chats

    @auth.middleware
    def post(token_data, self):
        chat_session_id = request.json.get('chat_session_id')
        #先获取聊天id
        if not chat_session_id:
            raise ChatMissingParamsError()

        chat_session = db.session.query(ChatSession).filter_by(
            id=chat_session_id, user_id=token_data['userId']).first()
            #聊天id和用户id查询数据库里的对话
        if not chat_session:
            return ChatMissingParamsError()

        #获取最后一个机器人创建的聊天，同时聊天里有一个关联question用于填充用户回复中的questionid
        last_question_chat = db.session.query(Chat).filter(
            Chat.chat_session_id == chat_session_id, Chat.user_id == token_data[
                'userId'], Chat.created_by == CreatedBy.bot
        ).order_by(desc('created_at')).first()
        #
        # if question is MCQ (i.e. has question.options), fill in the option ID of answer selected by user
        question_options = last_question_chat.question.options if last_question_chat and last_question_chat.question else False
        option_id = request.json.get('option_id')

        # if question is MCQ and no option is chosen, choose one based on closest Levenshtein distance with user input
        closest_option = None
        if question_options and not option_id and request.json.get('message_text'):
            closest_option = get_nearest_option(
                request.json.get('message_text'), question_options)
            option_id = closest_option.id if closest_option else None

        parameter = {
            'user_id': token_data['userId'],
            'chat_session_id': chat_session_id,
            'message_text': request.json.get('message_text'),
            'option_id': option_id,
            'created_by': CreatedBy.user,
            'question_id': last_question_chat.question_id if last_question_chat else None
        }

        #创建新聊天记录对象new_chat，将上述参数作为初始化参数，添加到数据库提交
        new_chat = Chat(**parameter)
        db.session.add(new_chat)
        db.session.commit()
        db.session.refresh(new_chat)
        #生成bot的回复
        reply_chat = ReplyGenerator(
            token_data['userId'], new_chat, chat_session, last_question_chat).get_reply()

        # Save response
        parameter = {
            'user_id': token_data['userId'],
            'chat_session_id': chat_session_id,
            'message_text': reply_chat['message_text'],
            'question_id': reply_chat['question_id'],
            'created_by': CreatedBy.bot
        }
        #创建新bot回复对象new_bot_response，添加到数据库提交
        new_bot_response = Chat(**parameter)
        db.session.add(new_bot_response)
        db.session.commit()
        db.session.refresh(new_bot_response)

        # If no more questions to ask, set chat session to `ready` status
        if not reply_chat['question_id']:
            chat_session.status = Status.ready
            db.session.commit()
            db.session.refresh(chat_session)
        #构建包含用户和机器人消息的json相应对象，表示当前会话状态，返回给客户端
        return jsonify({'user': {
            'id': new_bot_response.id,
            'messageText': new_chat.message_text,
            'createdBy': new_chat.created_by.name,
            'createdAt': new_chat.created_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'updatedAt': new_chat.updated_at.strftime('%Y-%m-%dT%H:%M:%S%z')
        }, 'bot': {
            'id': new_bot_response.id,
            'messageText': new_bot_response.message_text,
            'createdBy': new_bot_response.created_by.name,
            'createdAt': new_bot_response.created_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'updatedAt': new_bot_response.updated_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'options': reply_chat['options'],
        }, 'status': chat_session.status.name})


class ChatApi(Resource):
    #删除单个聊天记录，返回删除指定userid的成功的响应
    @auth.middleware
    def delete(token_data, self, id):
        db.session.query(Chat).filter_by(
            id=request.json.get('id'), user_id=token_data['userId']).first().delete()
        db.session.commit()
        return {"success": True}
    #获取单个聊天记录的信息，查找指定userid的聊天记录
    @auth.middleware
    def get(token_data, self, id):
        chat = db.session.query(Chat).filter_by(
            id=request.json.get('id'), user_id=token_data['userId']).first()
        return jsonify({'id': chat.id, 'message_text': chat.message_text, 'created_by': chat.created_by.strftime.name, 'updated_at': chat.updated_at.strftime('%Y-%m-%dT%H:%M:%S%z'), 'created_by': chat.created_by.strftime('%Y-%m-%dT%H:%M:%S%z')})

#该类用于生成聊天机器人的回复
class ReplyGenerator:
    def __init__(self, user_id, user_chat, chat_session, last_question_chat):
        self.user_id = user_id
        self.user_chat = user_chat
        self.chat_session = chat_session
        self.last_question_chat = last_question_chat
        self.prompts = ["Interesting. Could you tell me more?",
                        "Great. Tell me more.", "Interesting. Do you have anything more to add?"]
    #从数据库获取没有被问过的第一个问题
    def get_first_unasked_question(self):
        chats_subquery = db.session.query(Chat.id, Chat.question_id).filter(
            Chat.user_id == self.user_id, Chat.chat_session_id == self.chat_session.id, Chat.created_by == CreatedBy.bot).subquery()

        query = db.session.query(Question, chats_subquery)\
            .join(chats_subquery,
                  Question.id == chats_subquery.c.question_id,
                  isouter=True).subquery()
        question = db.session.query(Question).join(query, Question.id == query.c.id).filter(query.c.question_id.is_(None)).order_by(
            asc(query.c.order)).first()
        return question
    #计算用户对特定问题回答的总字符长度和回答次数
    def get_total_length(self):
        if self.user_chat and self.user_chat.question and self.user_chat.question.min_response_length and self.user_chat.created_by == CreatedBy.user and self.chat_session.chats:
            total_length = 0
            total_answers = 0
            for chat in self.chat_session.chats:
                if chat.question_id == self.user_chat.question_id and chat.created_by == CreatedBy.user:
                    total_length += len(chat.message_text)
                    total_answers += 1
            return total_length, total_answers
        return None, None
    #生成聊天机器人的回复，先决定是否发送提示，继续提问的话就调取下一个没被问过的问题
    def get_reply(self):
        # Handle open ended
        prompt = None
        if self.user_chat.question and self.user_chat.question.min_response_length:
            total_length, total_answers = self.get_total_length()
            is_complete = total_length >= self.user_chat.question.min_response_length if total_length else False
            if not is_complete and total_answers >= 3:
                is_complete = True
            prompt = random.choice(self.prompts) if not is_complete else None

            # Stay with current question
            if prompt:
                return {
                    "question_id": self.user_chat.question_id,
                    'message_text': prompt,
                    'options': None
                }

        # Handle subsequent questions
        first_unasked_question = self.get_first_unasked_question()

        if first_unasked_question:
            return {
                "question_id": first_unasked_question.id,
                'message_text': first_unasked_question.text,
                'options': first_unasked_question.get_options_dict()
            }
        else:
            return {
                "question_id": None,
                'message_text': 'Thank you for responding!',
                "options": None
            }


class ChatMissingParamsError(Exception):
    """ChatMissingParamsError error"""
