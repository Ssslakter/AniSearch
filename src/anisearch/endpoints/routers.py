from fastapi import APIRouter
from src.anisearch.startup import services
from src.anisearch.endpoints import admin


router = APIRouter()
api_prefix = "/api/v1"

router.include_router(admin.router, tags=["Admin"], prefix=api_prefix)


@router.get("/content", tags=["Content"])
async def get_relevant_content(query: str):
    return await services.search_anime(query)


@router.get("/content/{uid}", tags=["Content"])
def get_by_id(uid: int):
    return services.get_anime(uid)
