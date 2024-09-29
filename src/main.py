import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import topic_router, qa_router, chat_router, user_public_router, user_protected_router
from config import settings
from database import sessionmanager


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if settings.LOG_LEVEL == "DEBUG" else logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, docs_url="/api/docs")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Routers
app.include_router(topic_router)
app.include_router(user_public_router)
app.include_router(user_protected_router)
app.include_router(qa_router)
app.include_router(chat_router)


# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True, port=8000)
