from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import NoResultFound
from models import Chat


async def get_chat(db: AsyncSession, chat_id: int) -> Chat:
    chat = (await db.execute(
        select(Chat).where(Chat.id == chat_id)
    )).scalars().first()
    
    if not chat:
        raise NoResultFound(f"Chat with id {chat_id} not found.")
    return chat


async def get_chat_details(db: AsyncSession, chat_id: int) -> Chat:
    chat = (await db.execute(
        select(Chat)
        .where(Chat.id == chat_id)
        .options(
            joinedload(Chat.user), 
            joinedload(Chat.topic)
        )
    )).scalars().first()
    
    if not chat:
        raise NoResultFound(f"Chat with id {chat_id} not found.")
    return chat


async def get_chat_details_with_qas(db: AsyncSession, chat_id: int) -> Chat:
    chat = (await db.execute(
        select(Chat)
        .where(Chat.id == chat_id)
        .options(
            selectinload(Chat.qas),
            joinedload(Chat.topic), 
            joinedload(Chat.user)   
        )
    )).scalars().first()
    
    if not chat:
        raise NoResultFound(f"Chat with id {chat_id} not found.")
    return chat


async def get_all_chats_by_user(db: AsyncSession, user_id: int) -> list[Chat]:
    result = (await db.execute(
        select(Chat)
        .where(Chat.user_id == user_id)
        .options(joinedload(Chat.topic))
        .distinct()
    ))
    
    return result.scalars().unique().all()


async def get_all_chats(db: AsyncSession) -> list[Chat]:
    result = (await db.execute(
        select(Chat)
        .options(joinedload(Chat.topic))
        .options(joinedload(Chat.user))
        .distinct()
    ))
    
    return result.scalars().unique().all()


async def create_chat(db: AsyncSession, **kwargs) -> Chat:
    result = await db.execute(
        insert(Chat)
        .values(**kwargs)
        .returning(Chat)
        .options(joinedload(Chat.topic))
    )
    chat = result.scalars().first()

    if not chat:
        raise ValueError("Chat not created")
    return chat


async def delete_chat(db: AsyncSession, chat_id: int) -> None:
    result = await db.execute(delete(Chat).where(Chat.id == chat_id))
    
    if result.rowcount == 0:
        raise NoResultFound(f"Chat with id {chat_id} not found.")
