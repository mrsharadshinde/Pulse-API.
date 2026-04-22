from pydantic import BaseModel, Field, field_validator, ConfigDict, EmailStr
from typing import Annotated, Optional
from datetime import datetime

from app.schema.user_schema import UserResponse


# 1. THE FOUNDATION: Only the universally shared fields
class PostBase(BaseModel):
    title: Annotated[str, Field(..., alias='title', description='The title of the post')]
    content: Annotated[str, Field(..., description='The content of the post')]
    published: Annotated[bool, Field(default=True, description='Whether or not the post is published')]
    @field_validator('title', 'content')
    @classmethod
    def validate_text_field(cls, value: str):
        if not value.strip():
            raise ValueError('The value cannot be empty')
        if len(value) < 5:
            raise ValueError('The value cannot be less than 5 characters')
        return value


# 2. CREATE POST: Inherits the foundation + adds 'published'
class CreatePost(PostBase):
    pass

# 3. UPDATE POST: Needs everything completely optional
class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None


# 4. POST RESPONSE: Inherits the foundation + adds database fields (No 'published'!)
class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int
    owner : UserResponse

    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    Posts: PostResponse  # <-- Notice the 's' to match your SQLAlchemy model name!
    votes: int

    model_config = ConfigDict(from_attributes=True)

