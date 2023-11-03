from app.controllers.chat import ChatApi, ChatsApi
from app.controllers.user import LoginApi, LogoutApi, RegisterApi, UserApi
from app.controllers.chat_session import ChatSessionApi, ChatSessionsApi
from app.controllers.result import GenerateResultsApi, ResultApi, ResultRatingApi
from app.controllers.product import ProductsApi


# 定义不同路由和对应资源，如何响应不同HTTP请求
def initialize_routes(api):
    """Initialize routes"""
    api.add_resource(LoginApi, "/api/login")
    api.add_resource(LogoutApi, "/api/logout")
    api.add_resource(RegisterApi, "/api/register")
    api.add_resource(UserApi, "/api/user")

    api.add_resource(ChatSessionsApi, "/api/chat_sessions")
    api.add_resource(ChatSessionApi, "/api/chat_sessions/<int:id>")
    api.add_resource(
        GenerateResultsApi, "/api/chat_sessions/<int:chat_session_id>/results"
    )
    api.add_resource(
        ResultApi, "/api/chat_sessions/<int:chat_session_id>/results/<int:id>"
    )
    api.add_resource(ResultRatingApi, "/api/results/<int:id>")
    api.add_resource(ProductsApi, "/api/products/<string:id>")

    api.add_resource(ChatsApi, "/api/chats")
    api.add_resource(ChatApi, "/api/chats/<int:id>")
