from . import Base
from sqlalchemy import Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class QuestionAnswer(Base):
    __tablename__ = 'question_answers'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    
    question: Mapped[str] = mapped_column(Text, nullable=False)
    q_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    a_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    a_source: Mapped[str] = mapped_column(String(100), nullable=False)
    
    chat = relationship('Chat', back_populates='qas')
