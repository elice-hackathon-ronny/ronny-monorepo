from fastapi import status, HTTPException
from src.model.user import User
from src.model.debate import Debate, DebateMessage
from src.repository.mongo import database
from src.dto.debate import DebateForm, DebateMessageForm
import src.service.debate_mapper as debate_mapper
import src.service.chatgpt_service as chatgpt_service
from typing import Any
from bson.objectid import ObjectId
from bson import json_util

def start_debate(form: DebateForm) -> str:
    debates = database.get_debates()
    return str(debates.insert_one(debate_mapper.make_debate(form)).inserted_id)


def continue_debate(debate_id : str, form: DebateMessageForm) -> DebateMessageForm:

    debates = database.get_debates()

    # https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
    query_filter = {'_id': ObjectId(debate_id)}


    # list(debates.find(query_filter, sort="asdf"))

    new_value = { '$push': { 'messages': { '$each': debate_mapper.make_debate_messages(form) } } }
    update_result1 = debates.update_one(query_filter, new_value)


    debate = debates.find_one(query_filter)
    if debate is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="debate not found"
        )
    
    new_message = chatgpt_service.get_new_message(debate, debate['messages'])


    new_value = { '$push': { 'messages': { '$each': debate_mapper.make_debate_messages(new_message, by_user=False) } } }
    update_result2 = debates.update_one(query_filter, new_value)
    
    if update_result1.acknowledged and update_result2.acknowledged:
        #TODO throw error
        pass

    return new_message
    
def end_debate(debate_id : str, form: DebateMessageForm)-> DebateMessageForm:
    debates = database.get_debates()

    # https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
    query_filter = {'_id': ObjectId(debate_id)}


    new_value = { '$push': { 'messages': { '$each': debate_mapper.make_debate_messages(form, end=True) } } }
    update_result1 = debates.update_one(query_filter, new_value)
    

    debate = debates.find_one(query_filter)
    if debate is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="debate not found"
        )

    new_message = chatgpt_service.get_end_message(debate, debate.messages)


    if not update_result1.acknowledged():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal error"
        )
    
    new_value = { '$push': { 'messages': { '$each': debate_mapper.make_debate_messages(new_message, by_user=False) } } }
    update_result2 = debates.update_one(query_filter, new_value)

    if not update_result2.acknowledged():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal error"
        )

    return new_message

def get_debate(debate_id:str) -> Debate :
    
    debates = database.get_debates()
    # https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
    
    query_filter = {'_id': ObjectId(debate_id)}
    
    return debates.find_one(query_filter)


def get_debate_summary(debate_id:str) -> Debate :
    
    debates = database.get_debates()
    # https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
    
    query_filter = {'_id': ObjectId(debate_id)}
    
    debate = debates.find_one(query_filter)
    if  debates.find_one is None :
        pass
    print(debate)
    return debate
