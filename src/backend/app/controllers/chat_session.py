from flask import current_app, jsonify, Response, request
from flask_restful import Resource

from app.models.chat_session import ChatSession
from app.models.chat import Chat, CreatedBy
from app.models.user import User

from app.middlewares.auth import Auth


from app.db import db


auth = Auth()

#映射聊天会话对象：会话id,名称，状态，用户id等
def map_chat_sessions(chat_session):
    return {
        'id': chat_session.id,
        'name': chat_session.name,
        'status': chat_session.status.name,
        'userId': chat_session.user_id,
        'createdAt': chat_session.created_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'updatedAt': chat_session.updated_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
    }

#映射聊天记录：记录id，消息，用户id，创建者，时间等
def map_chats(chat):
    return {
        'id': chat.id,
        'messageText': chat.message_text,
        'userId': chat.user_id,
        'createdBy': chat.created_by.name,
        'createdAt': chat.created_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'updatedAt': chat.updated_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'options': chat.get_options_dict()
    }

#用于处理与聊天会话列表相关的http请求 get是获取用户所有聊天会话，post是创建新的聊天会话
class ChatSessionsApi(Resource):
    @auth.middleware
    def get(token_data, self):
        chat_sessions = db.session.query(ChatSession).filter_by(
            user_id=token_data['userId']).all()
        return jsonify(list(map(map_chat_sessions, chat_sessions)))

    @auth.middleware
    def post(token_data, self):
        parameter = {
            'user_id': token_data['userId'],
            'name': request.json.get('name')
        }
        object_to_insert = ChatSession(**parameter)
        db.session.add(object_to_insert)

        db.session.commit()
        db.session.refresh(object_to_insert)

        # Update user's latest chat session
        user = User.query.filter_by(id=token_data['userId']).first()
        user.last_chat_session_id = object_to_insert.id
        db.session.commit()

        # Add intro chat message
        intro_chat_parameter = {
            'user_id': token_data['userId'],
            'chat_session_id': object_to_insert.id,
            'message_text': 'Welcome to the WineBot! We can recommend the most suitable red wine for you. you just need to answer a few questions. All you need to do is answer a few simple questions. Shall we begin?',
            'created_by': CreatedBy.bot,
            'question_id': None
        }
        intro_chat = Chat(**intro_chat_parameter)
        db.session.add(intro_chat)
        db.session.commit()
        db.session.refresh(intro_chat)

        return jsonify({
            'id': object_to_insert.id,
            'name': object_to_insert.name,
            'status': object_to_insert.status.name,
            'userId': object_to_insert.user_id,
            'createdAt': object_to_insert.created_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'updatedAt': object_to_insert.updated_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'chats': [map_chats(intro_chat)]
        })

#处理与单个聊天会话相关的http请求。get是获取单个聊天会话详细信息，delete是删除
class ChatSessionApi(Resource):

    @auth.middleware
    def delete(token_data, self, id):
        db.session.query(ChatSession).filter_by(
            id=id, user_id=token_data['userId']).first().delete()
        db.session.commit()
        return {"success": True}

    @auth.middleware
    def get(token_data, self, id):
        chat_session = db.session.query(ChatSession).filter_by(
            id=id, user_id=token_data['userId']).join(Chat, ChatSession.id == Chat.chat_session_id, isouter=True).first()

        return jsonify({
            'id': chat_session.id,
            'name': chat_session.name,
            'status': chat_session.status.name,
            'userId': chat_session.user_id,
            'createdAt': chat_session.created_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'updatedAt': chat_session.updated_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'chats': list(map(map_chats, chat_session.chats))
        })
