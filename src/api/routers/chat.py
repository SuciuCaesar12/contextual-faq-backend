from api.dependencies.db import DBSessionDep
from api.dependencies.jwt import verify_token
import services.chat as chat_service
from schemas.chat import *
from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/api/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(verify_token)]
)


@router.get(
    '/',
    response_model=ChatSchema,
)
async def get_chat(db_session: DBSessionDep, id: int):
    return await chat_service.get_chat(db_session, id)


@router.get(
    '/details',
    response_model=ChatDetailsSchema,
)
async def get_chat_details(db_session: DBSessionDep, id: int):
    return await chat_service.get_chat_details(db_session, id)


@router.get(
    '/details/qas',
    response_model=ChatDetailsWithQAsSchema,
)
async def get_chat_details_with_qas(db_session: DBSessionDep, id: int):
    return await chat_service.get_chat_details_with_qas(db_session, id)


@router.get(
    '/user-all/details',
    response_model=list[ChatDetailsSchema],
)
async def get_all_chats_by_user(db_session: DBSessionDep, user_id: int):
    return await chat_service.get_all_chats_by_user(db_session, user_id)

@router.get(
    '/all/details',
    response_model=list[ChatDetailsSchema],
)
async def get_all_chats(db_session: DBSessionDep):
    return await chat_service.get_all_chats(db_session)


@router.post(
    '/',
    response_model=ChatDetailsSchema,
)
async def create_chat(db_session: DBSessionDep, new_chat_data: CreateChatRequest):
    created_chat = await chat_service.create_chat(db=db_session, **new_chat_data.model_dump())
    
    await db_session.commit()
    await db_session.refresh(created_chat)
    return created_chat


@router.delete(
    "/",
    response_model=dict,
)
async def delete_chat(db_session: DBSessionDep, id: int):
    await chat_service.delete_chat(db_session, id)
    
    await db_session.commit()
    return {"message": "Chat deleted"}

