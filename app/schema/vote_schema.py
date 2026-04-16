from pydantic import BaseModel, Field

class Vote(BaseModel):
    post_id: int
    dir: int = Field(ge=0, le=1, description="Direction of vote: 1 for like, 0 for unlike")
    