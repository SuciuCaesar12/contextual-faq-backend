from langchain_openai import OpenAIEmbeddings   
from config import settings

embedding_model = OpenAIEmbeddings(model='text-embedding-3-small', dimensions=256, api_key=settings.OPENAI_API_KEY)
