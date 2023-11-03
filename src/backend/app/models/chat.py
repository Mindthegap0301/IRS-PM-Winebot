from sqlalchemy import func
from sqlalchemy.orm import relationship
from dataclasses import dataclass
import enum
from app.models.user import User
from app.models.chat_session import ChatSession
from app.models.question import Question
from app.models.option import Option
from app.db import db

#枚举类，表示创建者是用户或机器人
class CreatedBy(enum.Enum):
    user = 1
    bot = 2


@dataclass
class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id), nullable=False)
    chat_session_id = db.Column(db.ForeignKey(ChatSession.id),
                                nullable=False)
    message_text = db.Column(db.String)
    question_id = db.Column(db.ForeignKey(Question.id))
    option_id = db.Column(db.ForeignKey(Option.id))
    created_by = db.Column(
        db.Enum(CreatedBy), nullable=False, default=CreatedBy.bot)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), onupdate=func.now())

    chat_session = relationship("ChatSession", back_populates="chats")
    question = relationship("Question")
    option = relationship("Option")

    def get_options_dict(self):
        if self.created_by == CreatedBy.bot and self.question and self.question.options:
            return list(map(lambda option: {'id': option.id, 'order': option.order, 'value': option.value, 'data_type': option.data_type.name, 'label': option.label}, self.question.options))

# Create / update timestamps: https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
