from typing import Any, Dict

from fastapi import APIRouter, Body
import json
from bson import json_util

from src.service import user_service
from src.service import debate_service
from src.dto.debate import DebateForm, DebateMessagePairForm, SimpleDebateMessageForm, SingleDebateMessage
from src.model.debate import Debate
from src.routes.metadata import response_example

router = APIRouter(tags=['debate'], prefix="/api/debate")


@router.post("", responses=response_example.start_debate_example())
def start_debate(form : DebateForm = Body()) -> Dict:
    return debate_service.start_debate(form)


@router.get("/{debate_id}")
def get_debate(debate_id: str) -> Any:
    return parse_json(debate_service.get_debate(debate_id))


@router.post("/{debate_id}/message", responses= response_example.continue_debate_example())
def add_debate(debate_id: str, form : SimpleDebateMessageForm) -> bool:
    return debate_service.add_debate(debate_id,form)

@router.get("/{debate_id}/message")
def get_debate_message(debate_id: str) -> SingleDebateMessage:
    return debate_service.get_debate_message(debate_id)


@router.get("/{debate_id}/conclusion")
def conclude_debate(debate_id):
    return debate_service.end_debate(debate_id)

@router.post("/{debate_id}/conclusion", responses = response_example.end_debate_example())
def conclude_debate_with(debate_id: str, form : SimpleDebateMessageForm) -> SingleDebateMessage:
    return debate_service.end_debate_with(debate_id,form)

@router.get("/{debate_id}/summary")
def get_debate_summary(debate_id : str) -> str :
    return parse_json(debate_service.get_debate_summary(debate_id))

def parse_json(data):
    return json.loads(json_util.dumps(data))