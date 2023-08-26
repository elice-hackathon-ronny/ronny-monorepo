from typing import List, Dict

from src.dto.debate import DebateForm, DebateMessageForm
from src.model.debate import Debate, DebateMessage
from datetime import datetime
import json
from bson.objectid import ObjectId

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(MyEncoder, self).default(obj)
    

def make_debate(
        form :DebateForm
    ) -> Dict:
    
    result = form.model_dump()
    result['created_at'] = datetime.now()
    result['messages'] = []
    return result

def make_debate_messages(
        form: DebateMessageForm,
        by_user = True
) -> List[Dict]:
    
    timestamp= datetime.now()
    author = "user" if by_user else "assistant"

    results = [
        DebateMessage(
            message=form.counter,
            message_type = "counter",
            author = author,
            created_at = timestamp
        ).model_dump(),
        DebateMessage(
            message=form.arg,
            message_type = "arg",
            author = author,
            created_at = timestamp
        ).model_dump(),
    ]

    return results

def extract_debate_gpt_message():
    pass

def encode_debate(
        debate : Debate
):
    pass
    