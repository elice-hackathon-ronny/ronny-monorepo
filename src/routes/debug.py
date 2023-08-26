from fastapi import APIRouter
from src.model.user import User
from src.service import user_service
from src.env import mongo_db_url


router = APIRouter(tags=['debug'], prefix="/api/debug")


@router.get("/mongo/url")
def register() -> str:
    return mongo_db_url()
