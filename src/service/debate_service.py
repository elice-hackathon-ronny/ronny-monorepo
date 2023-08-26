from fastapi import status, HTTPException
from src.model.user import User
from src.model.debate import Debate, DebateMessage
from src.repository.mongo import database
from src.dto.debate import DebateForm, DebateMessagePairForm, SingleDebateMessage, SimpleDebateMessageForm
import src.service.debate_mapper as debate_mapper
import src.service.chatgpt_service as chatgpt_service
from typing import Any
from bson.objectid import ObjectId
from bson import json_util

def start_debate(form: DebateForm) -> SingleDebateMessage:
    debates = database.get_debates()
    
    inserted_id = str(debates.insert_one(debate_mapper.make_debate(form)).inserted_id)
    
    query_filter = {'_id': ObjectId(inserted_id)}
    debate = debates.find_one(query_filter)
    if debate is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="debate not found"
    )
    
    new_message = chatgpt_service.get_new_message(debate, debate['messages'])
    
    new_debate_message = SingleDebateMessage(
        message = new_message,
        message_type="arg",
        author="assistant"
    )

    new_value = { '$push': { 'messages':  debate_mapper.make_gpt_message(new_debate_message)  } }
    update_result = debates.update_one(query_filter, new_value)
    if not update_result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal error"
        )

    return {"debate_id" : inserted_id, "message": new_debate_message}


def add_debate(debate_id : str, form: SimpleDebateMessageForm) -> bool:

    debates = database.get_debates()

    # https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
    query_filter = {'_id': ObjectId(debate_id)}


    new_value = { '$push': { 'messages': debate_mapper.make_debate_message(form)  } }
    update_result = debates.update_one(query_filter, new_value)
    
    return update_result.acknowledged

def get_debate_message(debate_id:str)->SingleDebateMessage:
    debates = database.get_debates()
    # https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
    query_filter = {'_id': ObjectId(debate_id)}
    debate = debates.find_one(query_filter)
    
    if debate is None or len(debate['messages'])==0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="debate not found"
        )
    
    
    new_message = chatgpt_service.get_new_message(debate, debate['messages'])
    print("nnew_amaefwefwe!!!", new_message)

    message_type = "arg" if debate['messages'][-1]['author']=="assistant" else "counter"
    new_debate_message = SingleDebateMessage(
        message = new_message,
        message_type=message_type,
        author="assistant"
    )

    new_value = { '$push': { 'messages':  debate_mapper.make_gpt_message(new_debate_message)  } }
    update_result = debates.update_one(query_filter, new_value)
    if not update_result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal error"
        )
    
    return new_debate_message


def end_debate_with(debate_id : str, form: SimpleDebateMessageForm)-> SingleDebateMessage:
    debates = database.get_debates()

    # https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
    query_filter = {'_id': ObjectId(debate_id)}


    new_value = { '$push': { 'messages': debate_mapper.make_debate_message(form, end=True)  } }
    update_result = debates.update_one(query_filter, new_value)
    
    if not update_result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal error"
        )

    debate = debates.find_one(query_filter)
    if debate is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="debate not found"
        )
    
    new_message = chatgpt_service.get_new_message(debate, debate['messages'],end=True)

    new_debate_message = SingleDebateMessage(
        message = new_message,
        message_type="arg",
        author="assistant"
    )

    
    new_value = { '$push': { 'messages':  debate_mapper.make_gpt_message(new_debate_message)  } }
    update_result = debates.update_one(query_filter, new_value)
    if not update_result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal error"
        )
    
    return new_debate_message

def end_debate(debate_id : str)->SingleDebateMessage:
    debates = database.get_debates()

    # https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
    query_filter = {'_id': ObjectId(debate_id)}

    debate = debates.find_one(query_filter)
    if debate is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="debate not found"
        )
    
    new_message = chatgpt_service.get_new_message(debate, debate['messages'],end=True)

    new_debate_message = SingleDebateMessage(
        message = new_message,
        message_type="arg",
        author="assistant"
    )

    
    new_value = { '$push': { 'messages':  debate_mapper.make_gpt_message(new_debate_message)  } }
    update_result = debates.update_one(query_filter, new_value)
    if not update_result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal error"
        )
    
    return new_debate_message

def get_debate(debate_id:str) -> Debate :
    
    debates = database.get_debates()
    # https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
    
    query_filter = {'_id': ObjectId(debate_id)}
    
    return debates.find_one(query_filter)


def get_debate_summary(debate_id:str) -> str :
    
    debates = database.get_debates()
    # https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
    
    query_filter = {'_id': ObjectId(debate_id)}
    
    debate = debates.find_one(query_filter)
    if debate is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="debate not found"
        )
    
    new_message = chatgpt_service.get_new_message(debate, debate['messages'],end=True)

    return new_message
