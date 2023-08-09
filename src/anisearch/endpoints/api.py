from fastapi import APIRouter
from src.anisearch.endpoints import admin, content, user


router = APIRouter()
api_prefix = "/api/v1"

router.include_router(admin.router, tags=["Admin"], prefix=api_prefix)
router.include_router(content.router, tags=["Content"], prefix=api_prefix)
router.include_router(user.router, tags=["User"], prefix=api_prefix)
