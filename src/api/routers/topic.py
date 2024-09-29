from api.dependencies.db import DBSessionDep
from api.dependencies.jwt import verify_token
import services.topic as topic_service
from schemas.topic import *
from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/api/topic",
    tags=["topics"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(verify_token)],
)


@router.get(
    "/",
    response_model=TopicSchema,
)
async def get(db_session: DBSessionDep, id: int):    
    return await topic_service.get_topic_by_id(db_session, id)


@router.get(
    "/all",
    response_model=list[TopicSchema],
)
async def get_all(db_session: DBSessionDep):
    return await topic_service.get_all_topics(db_session)


@router.get(
    "/details",
    response_model=TopicDetailsSchema,
)
async def get_details(db_session: DBSessionDep, id: int):
    return await topic_service.get_topic_by_id(db_session, id)


@router.get(
    "/all/details",
    response_model=list[TopicDetailsSchema],
)
async def get_all_details(db_session: DBSessionDep):
    return await topic_service.get_all_topics(db_session)


@router.get(
    "/available",
    response_model=list[TopicDetailsSchema],
)
async def get_available_topics_for_user(db_session: DBSessionDep, user_id: int):
    return await topic_service.get_available_topics_for_user(db_session, user_id)


@router.post(
    '/',
    response_model=TopicDetailsSchema,
)
async def create(db_session: DBSessionDep, new_topic_data: CreateTopicRequest):
    created_topic = await topic_service.create_topic(db_session, **new_topic_data.model_dump())
    
    await db_session.commit()
    await db_session.refresh(created_topic)
    return created_topic


@router.delete(
    "/",
    response_model=dict,
)
async def delete(db_session: DBSessionDep, id: int):
    await topic_service.delete_topic(db_session, id)
    
    await db_session.commit()
    return {"message": "Topic deleted"}

