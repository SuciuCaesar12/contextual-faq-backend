
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from models import QuestionAnswer as QA


async def create_qa(db: AsyncSession, **kwargs) -> QA:
    stmt = insert(QA).values(**kwargs).returning(QA)
    qa = (await db.execute(stmt)).scalars().first()
    
    if not qa:
        raise ValueError("QuestionAnswer not created")
    return qa
