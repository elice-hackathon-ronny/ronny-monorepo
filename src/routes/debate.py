from typing import Any, Dict

from fastapi import APIRouter, Body
import json
from bson import json_util

from src.service import user_service
from src.service import debate_service
from src.dto.debate import DebateForm, DebateMessageForm
from src.model.debate import Debate
from src.routes.metadata import response_example

router = APIRouter(tags=['debate'], prefix="/api/debate")


@router.post("", responses=response_example.start_debate_example())
def start_debate(form : DebateForm = Body()) -> Dict:
    return {'debate_id':debate_service.start_debate(form)}


@router.get("/{debate_id}")
def get_debate(debate_id: str) -> Any:
    return parse_json(debate_service.get_debate(debate_id))


@router.post("/{debate_id}", responses= response_example.continue_debate_example())
def continue_debate(debate_id: str, form : DebateMessageForm) -> Any:
    return debate_service.continue_debate(debate_id,form)

@router.post("/{debate_id}/conclusion", responses = response_example.end_debate_example())
def continue_debate(debate_id: str, form : DebateMessageForm) -> Any:
    return debate_service.end_debate(debate_id,form)

@router.get("/{debate_id}/summary")
def get_debate_summary(debate_id : str) -> Any :
    return parse_json(debate_service.get_debate_summary(debate_id))

def parse_json(data):
    return json.loads(json_util.dumps(data))