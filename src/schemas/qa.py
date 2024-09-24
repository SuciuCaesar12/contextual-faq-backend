from pydantic import BaseModel
from datetime import datetime


class CreateQAReq(BaseModel):
    chat_id: int
    question: str
    topic_name: str
    q_timestamp: datetime


class QASchema(BaseModel):
    chat_id: int
    
    question: str
    q_timestamp: datetime
    
    answer: str
    a_timestamp: datetime
    a_source: str
    
    model_config = dict(from_attributes=True)
