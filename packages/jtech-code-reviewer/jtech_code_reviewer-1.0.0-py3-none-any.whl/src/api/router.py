from fastapi import APIRouter

from src.api.v1 import code_review_controller
from src.infra.config.settings import Config

api_router = APIRouter()

api_router.include_router(code_review_controller.route, prefix=Config.API_V1_STR + "/code_review", tags=["code_review"])
