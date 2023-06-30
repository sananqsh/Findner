from fastapi import APIRouter
from . import partners

api_router = APIRouter()

api_router.include_router(partners.router, prefix="/partners", tags=["Partners"])
