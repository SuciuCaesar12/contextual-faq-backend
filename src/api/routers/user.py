from fastapi import APIRouter, Depends, HTTPException, status
from api.dependencies.db import DBSessionDep
import services.user as user_service
from schemas.user import *
from api.dependencies.jwt import (
    authenticate_user,
    create_access_token,
    verify_token,
    get_password_hash,
)
from datetime import timedelta, datetime, timezone
from config import settings


public_router = APIRouter(
    prefix="/api/user",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@public_router.post("/login", response_model=dict)
async def login_user(db_session: DBSessionDep, user_data: LoginRequest):
    user = await authenticate_user(user_data.username, user_data.password, db_session)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Set token expiration time
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expiry_time = datetime.now(timezone.utc) + access_token_expires
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    # Return the token, expiry time in ISO format
    return {
        "user_id": user.id,
        'role': user.role,
        "access_token": access_token,
        "token_type": "bearer",
        "expiry": expiry_time.isoformat()  # ISO 8601 format
    }


@public_router.post("/register", response_model=dict)
async def register_user(new_user_data: CreateUserRequest, db_session: DBSessionDep):
    new_user_data.password = get_password_hash(new_user_data.password)
    new_user = await user_service.create_user(db_session, **new_user_data.model_dump())
    
    await db_session.commit()
    await db_session.refresh(new_user)
    
    # Set token expiration time
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expiry_time = datetime.now(timezone.utc) + access_token_expires
    
    # Create access token
    access_token = create_access_token(
        data={"sub": new_user.username}, 
        expires_delta=access_token_expires
    )
    
    return {
        "user_id": new_user.id,
        'role': new_user.role,
        "access_token": access_token,
        "token_type": "bearer",
        "expiry": expiry_time.isoformat()  # ISO 8601 format
    }


protected_router = APIRouter(
    prefix="/api/user",
    tags=["users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(verify_token)],
)

@protected_router.get("/", response_model=UserSchema)
async def get_user(
    db_session: DBSessionDep,
    id: int
):
    return await user_service.get_user_by_id(db_session, id)


@protected_router.get("/all", response_model=list[UserDetailsSchema])
async def get_all_users(db_session: DBSessionDep):
    return await user_service.get_all_users(db_session)


@protected_router.get("/details", response_model=UserDetailsSchema)
async def get_user_details(
    db_session: DBSessionDep,
    id: int
):
    return await user_service.get_user_by_id(db_session, id)



@protected_router.get("/all/details", response_model=list[UserDetailsSchema])
async def get_all_users_details(db_session: DBSessionDep):
    return await user_service.get_all_users(db_session)


@protected_router.post("/", response_model=UserDetailsSchema)
async def create_user(
    db_session: DBSessionDep,
    new_user_data: CreateUserRequest
):
    new_user_data.password = get_password_hash(new_user_data.password)
    new_user = await user_service.create_user(db_session, **new_user_data.model_dump())
    
    await db_session.commit()
    await db_session.refresh(new_user)
    return new_user


@protected_router.put("/", response_model=UserDetailsSchema)
async def update_user(
    db_session: DBSessionDep,
    user_data: UpdateUserRequest
):
    user_data.password = get_password_hash(user_data.password)
    updated_user = await user_service.update_user(db_session, **user_data.model_dump())
    
    await db_session.commit()
    await db_session.refresh(updated_user)
    return updated_user


@protected_router.delete("/", response_model=dict)
async def delete_user(
    db_session: DBSessionDep,
    id: int
):
    await user_service.delete_user(db_session, id)
    
    await db_session.commit()
    return {"message": "User deleted"}


def get_routers():
    return [public_router, protected_router]
