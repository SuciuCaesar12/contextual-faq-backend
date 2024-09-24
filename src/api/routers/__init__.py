from .topic import router as topic_router
from .user import public_router as user_public_router, protected_router as user_protected_router
from .qa import router as qa_router
from .chat import router as chat_router