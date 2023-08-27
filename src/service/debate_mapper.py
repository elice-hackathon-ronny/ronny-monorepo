from typing import List, Dict

from src.dto.debate import DebateForm, DebateMessagePairForm, SingleDebateMessage,SimpleDebateMessageForm
from src.model.debate import Debate, DebateMessage, DebateSummary
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

def make_debate_message(
        form: SimpleDebateMessageForm,
        by_user = True,
        end = False
) -> Dict:
    
    timestamp= datetime.now()
    author = "user" if by_user else "assistant"
    
    result = DebateMessage(
        message = form.message,
        message_type = form.message_type,
        author = author,
        created_at = timestamp
    ).model_dump()
    return result

def make_gpt_message(chat : SingleDebateMessage):
    timestamp= datetime.now()
    result = DebateMessage(
                message=chat.message,
                message_type = chat.message_type,
                author = chat.author,
                created_at = timestamp
            ).model_dump()
    return result

def make_summary(debate_id :str, chat_summary:Dict)->DebateSummary:
    return DebateSummary(
        debate_id = debate_id,
        ronny_summary = chat_summary['ronny_summary'],
        user_summary = chat_summary['user_summary'],
        eval = chat_summary['eval']
    )

def make_summary_response(summary : DebateSummary)->Dict :
    return {
        'ronny_summary' : summary.ronny_summary,
        'user_summary' : summary.user_summary,
        'eval' : summary.eval
    }

def encode_debate(
        debate : Debate
):
    pass
    