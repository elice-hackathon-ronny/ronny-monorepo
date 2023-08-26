from pydantic import BaseModel, Field
from bson.objectid import ObjectId


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    user_id: str
