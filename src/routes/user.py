from fastapi import APIRouter, Body
from src.model.user import User
from src.service import user_service


router = APIRouter(tags=['user'], prefix="/api/user")


@router.post("/")
def register(user: User = Body()) -> bool:
    return user_service.register(user)


@router.get(":{user_id}")
def login(user_id: str) -> bool:
    user = User(user_id=user_id)
    return user_service.get_user(user)


@router.delete(":{user_id}")
def delete_user(user_id: str) -> bool:
    user = User(user_id=user_id)
    return user_service.delete_user(user)
