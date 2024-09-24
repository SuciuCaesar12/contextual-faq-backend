from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from models import Topic, Chat
from sqlalchemy.orm import aliased


async def create_topic(db: AsyncSession, **kwargs) -> Topic:
    stmt = insert(Topic).values(**kwargs).returning(Topic)
    topic = (await db.execute(stmt)).scalars().first()
    
    if not topic:
        raise ValueError("Topic not created")
    return topic


async def get_topic_by_id(db: AsyncSession, id: int) -> Topic:
    return await db.get(Topic, id)


async def get_all_topics(db: AsyncSession) -> list[Topic]:
    return (await db.execute(select(Topic))).scalars().all()


async def delete_topic(db: AsyncSession, id: int):
    return await db.execute(delete(Topic).where(Topic.id == id))
    
async def get_available_topics_for_user(db: AsyncSession, user_id: int) -> list[Topic]:
    ChatAlias = aliased(Chat)
    stmt = (
        select(Topic)
        .outerjoin(ChatAlias, (Topic.id == ChatAlias.topic_id) & (ChatAlias.user_id == user_id))
        .where(ChatAlias.id.is_(None))
    )

    return (await db.execute(stmt)).scalars().all()

