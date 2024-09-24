from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: int
    username: str
    role: str
    model_config = ConfigDict(from_attributes=True)


class UserDetailsSchema(UserSchema):
    password: str
    
    
class LoginRequest(BaseModel):
    username: str
    password: str


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str


class UpdateUserRequest(BaseModel):
    id: int
    username: str
    password: str
    role: str
