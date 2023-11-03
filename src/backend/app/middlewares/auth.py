from flask import current_app, make_response
from flask import request
from functools import wraps
import jwt

#实现身份验证和授权中间件
class Auth:
    def middleware(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            JWT_SECRETKEY = current_app.config.get('JWT_SECRETKEY')
            #从flask获取密钥
            header_token = request.headers.get("Authorization")
            header_token = None if header_token is None else header_token.split(" ")[
                1]

            token = header_token if header_token else request.cookies.get(
                'x-auth-token')
            token_data = None
            if not token:
                raise TokenInvalid()
            try:
                token_data = jwt.decode(
                    token, key=JWT_SECRETKEY, algorithms='HS256')
            except jwt.ExpiredSignatureError:
                raise Unauthorized()
            except jwt.InvalidTokenError:
                raise TokenInvalid()
            return func(token_data, *args, **kwargs)
        return decorator


class Unauthorized(Exception):
    """Token Invalid Exception"""


class TokenInvalid(Exception):
    """Token Invalid Exception"""
