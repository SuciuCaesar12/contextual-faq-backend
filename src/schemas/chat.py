from pydantic import BaseModel, ConfigDict
from schemas.qa import QASchema
from schemas.topic import TopicDetailsSchema
from schemas.user import UserSchema
from typing import Optional


class ChatSchema(BaseModel):
    id: int
    user_id: int
    topic_id: int
    model_config = ConfigDict(from_attributes=True)


class ChatDetailsSchema(BaseModel):
    id: int
    user: Optional[UserSchema] = None
    topic: TopicDetailsSchema
    model_config = ConfigDict(from_attributes=True)


class ChatDetailsWithQAsSchema(ChatDetailsSchema):
    qas: list[QASchema]


class CreateChatRequest(BaseModel):
    user_id: int
    topic_id: int