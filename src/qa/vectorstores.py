from langchain_postgres.vectorstores import PGVector
from langchain.docstore.document import Document
from langchain.indexes import SQLRecordManager, aindex
from langchain_core.embeddings import Embeddings
from typing import List, Tuple

from qa.embeddings import embedding_model
from database import get_db_engine


class TopicPGVector:
    
    def __init__(self, topic: str, embeddings: Embeddings = embedding_model):
        self.topic = topic
        self.collection_name = f'collection_{topic}'
        self.embeddings = embeddings

        self.vectorstore = PGVector(
            embeddings=self.embeddings,
            connection=get_db_engine(),
            collection_name=self.collection_name,
            async_mode=True
        )
        
        self.namespace = f'pgvector/{topic}'
        self.record_manager = SQLRecordManager(
            self.namespace, engine=get_db_engine(), async_mode=True
        )
    
    async def initialize(self):
        await self.record_manager.acreate_schema()

    async def add(self, docs: List[Document], cleanup = None):
        return await aindex(docs, self.record_manager, self.vectorstore, cleanup=cleanup)

    async def asimilarity_search_with_score(self, question: str) -> List[Tuple[Document, float]]:
        return await self.vectorstore.asimilarity_search_with_score(query=question, k=1)

