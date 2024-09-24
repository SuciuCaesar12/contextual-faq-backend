from . import Base
from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Chat(Base):
    __tablename__ = 'chats'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    topic_id: Mapped[int] = mapped_column(ForeignKey('topics.id', ondelete='CASCADE'), nullable=False)
    
    user = relationship('User', back_populates='chats', lazy='joined')
    topic = relationship('Topic', back_populates='chats')
    qas = relationship('QuestionAnswer', back_populates='chat')

    __table_args__ = (
        UniqueConstraint('user_id', 'topic_id', name='uq_user_topic'),
    )
