from fastapi import APIRouter

from src.api.endpoints import debate

api_router = APIRouter()
api_router.include_router(debate.router, prefix="/debates", tags=["debates"])
