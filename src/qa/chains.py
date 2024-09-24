from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_community.docstore.document import Document
from langchain_openai import ChatOpenAI
from typing import Dict, Any
from datetime import datetime

from qa.vectorstores import TopicPGVector
from config import settings


FAIL_TEMPLATE_ANSWER = 'I am sorry, I could not find an answer on this topic. Try again.'


def create_topic_classifier():
    template = """Given the user question below, is the question {topic} related? 
    Classify the question as '{topic}' or 'Other'.
    
    Respond with either 'Other' or '{topic}'.

    <question>
    {question}
    </question>

    Classification:"""
    
    return (
        PromptTemplate.from_template(template) | 
        ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=settings.OPENAI_API_KEY) | 
        StrOutputParser()
    )
    

def initialize_chains():
    openai_chain = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                '''You are here to answer any questions you are asked. 
                Be concise and informative. Do not provide more information than necessary.''',
            ),
            ("human", "{question}"),
        ]
    ) | ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=settings.OPENAI_API_KEY)
    
    classifier_chain = {
        'classified_topic': create_topic_classifier(),
        'question': lambda x: x['question']
    }
    
    return openai_chain, classifier_chain

openai_chain, classifier_chain = initialize_chains()


async def route_answer(info: Dict[str, Any]) -> Dict[str, str]:
    question: str = info.get('question')
    classified_topic: str = info.get('classified_topic')

    if classified_topic.upper() == 'OTHER':
        return {
            'answer': FAIL_TEMPLATE_ANSWER,
            'a_source': 'N/A',
            'a_timestamp': datetime.now().isoformat() + 'Z'
        }
    
    vectorstore = TopicPGVector(topic=classified_topic)
    await vectorstore.initialize()
    matched_doc = await vectorstore.asimilarity_search_with_score(question)
    
    if matched_doc:
        [(doc, score)] = matched_doc
        if score < settings.SIMILARITY_THRESHOLD:
            return {
                'answer': doc.metadata['answer'],
                'a_source': 'SYSTEM',
                'a_timestamp': datetime.now().isoformat() + 'Z'
            }

    answer = openai_chain.invoke({"question": question}).content
    
    await vectorstore.add(
        docs=[Document(page_content=question, metadata={"answer": answer})]
    )
    
    return {
        'answer': answer,
        'a_source': 'OPENAI',
        'a_timestamp': datetime.now().isoformat() + 'Z'
    }

final_chain = classifier_chain | RunnableLambda(route_answer)
