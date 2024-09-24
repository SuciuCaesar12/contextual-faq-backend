from pydantic import BaseModel, ConfigDict


class TopicSchema(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TopicDetailsSchema(TopicSchema):
    name: str
    

class CreateTopicRequest(BaseModel):
    name: str
