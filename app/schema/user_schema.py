from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Annotated, Optional


# user schema
class CreateUser(BaseModel):
    name: Annotated[str, Field(description='The name of the user')]
    email: Annotated[EmailStr, Field( description='The email address of the user')]
    username: Annotated[str, Field(description='The username of the user')]
    password: Annotated[str, Field( description='The password of the user')]

class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class UserOutWithPosts(BaseModel):
    user: UserResponse
    post_count: int


class UpdateUser(BaseModel):
    name: str = None
    email: EmailStr = None
    username: str = None
    password: str = None

class UserLogin(BaseModel):
    username: str
    password: str

# The Token schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None