from fastapi import APIRouter
from src.anisearch.endpoints import admin


router = APIRouter()
api_prefix = "/api/v1"

router.include_router(admin.router, tags=["Admin"], prefix=api_prefix)
