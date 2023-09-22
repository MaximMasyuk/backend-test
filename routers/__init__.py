from fastapi import APIRouter
from routers.registration import app as register

api_v1_router = APIRouter(prefix="/api/v1")


api_v1_router.include_router(register)