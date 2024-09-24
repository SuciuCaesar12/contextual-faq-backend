# need access to this before importing models
from database import Base

from .topic import Topic
from .user import User
from .qa import QuestionAnswer
from .chat import Chat