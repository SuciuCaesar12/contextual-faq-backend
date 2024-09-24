from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from models import User


async def get_user_by_id(db: AsyncSession, id: int) -> User:
    return await db.get(User, id)


async def get_user_by_username(db: AsyncSession, username: str) -> User:
    return (await db.execute(select(User).where(User.username == username))).scalars().first()


async def get_all_users(db: AsyncSession) -> list[User]:
    return (await db.execute(select(User))).scalars().all()


async def create_user(db: AsyncSession, **kwargs):
    stmt = insert(User).values(**kwargs).returning(User)
    user = (await db.execute(stmt)).scalars().first()

    if not user:
        raise ValueError("User not created")
    return user


async def update_user(db: AsyncSession, id: int, **kwargs) -> User:
    stmt = update(User).where(User.id == id).values(**kwargs).returning(User)
    updated_user = (await db.execute(stmt)).scalars().first()

    if not updated_user:
        raise ValueError("User not updated")
    return updated_user


async def delete_user(db: AsyncSession, id: int):
    return await db.execute(delete(User).where(User.id == id))
