from api.dependencies.db import DBSessionDep
from api.dependencies.jwt import verify_token
import services.qa as qa_service
from schemas.qa import *
from fastapi import APIRouter, Depends
from qa.chains import final_chain
from typing import List


router = APIRouter(
    prefix="/api/qa",
    tags=["qa"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(verify_token)]
)


@router.post(
    '/',
    response_model=QASchema,
)
async def create_qa(db_session: DBSessionDep, new_qa_data: CreateQAReq):
    chain_result = await final_chain.ainvoke({"question": new_qa_data.question, 'topic': new_qa_data.topic_name})
    
    qa_complete = QASchema.model_validate({
        **new_qa_data.model_dump(exclude={'topic_name'}),
        **chain_result
    })
    
    created_qa = await qa_service.create_qa(db_session, **qa_complete.model_dump())
    
    await db_session.commit()
    await db_session.refresh(created_qa)
    
    return created_qa
