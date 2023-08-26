from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from datetime import datetime
from typing import List, Optional

# class UserForm(BaseModel):
#     user_id : str

class DebateForm(BaseModel):
    subject : str
    level: str
    position : str

class DebateMessagePairForm(BaseModel):
    counter: Optional[str] = None
    arg : str

# class DebateMessageResponse(BaseModel):
#     message: str
#     message_type: str
#     author : str
#     created_at: datetime

# class DebateResponse(BaseModel):
#     id : str
#     subject : str
#     level : str
#     position : str
#     created_at : datetime
#     messages: List[DebateMessageResponse]

class SingleDebateMessage(BaseModel):
    message: str
    message_type: str
    author : str

class SimpleDebateMessageForm(BaseModel):
    message : str
    message_type : str