from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from datetime import datetime
from typing import List, Optional



class DebateMessage(BaseModel):
    message: Optional[str]
    message_type: str
    author : str
    created_at: datetime


class Debate(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    subject : str
    level : str
    position : str
    created_at : datetime
    messages: List[DebateMessage]
    


class DebateSummary(BaseModel):
    debate_id : str
    ronny_summary : str
    user_summary : str
    eval : str