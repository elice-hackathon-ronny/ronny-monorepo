from fastapi import status, HTTPException
from src.model.user import User
from src.repository.mongo import database


def register(user: User) -> bool:
    users = database.get_users()

    # https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
    query_filter = {'user_id': user.user_id}
    if users.count_documents(query_filter) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user id already exists"
        )

    return users.insert_one(user.model_dump()) is not None


def get_user(user: User) -> bool:
    users = database.get_users()

    # https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
    query_filter = {'user_id': user.user_id}
    return users.count_documents(query_filter) > 0


def delete_user(user: User) -> bool:
    users = database.get_users()

    # https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
    query_filter = {'user_id': user.user_id}
    if users.count_documents(query_filter) > 0:
        return users.delete_one(query_filter).deleted_count > 0

    return False
