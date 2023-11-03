from typing import Optional

from pydantic import BaseModel

#验证用户登陆请求，响应身份验证令牌
class LoginParms(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str

#验证用户注册请求，响应令牌
class RegisterParams(BaseModel):
    username: str
    email: str
    password: str


class RegisterResponse(BaseModel):
    token: str

#表示用户信息
class UserParams(BaseModel):
    id: int
    email: str
    username: str
    last_chat_session_id: int


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    last_chat_session_id: int
