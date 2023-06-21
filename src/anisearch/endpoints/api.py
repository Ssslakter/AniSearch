from fastapi import APIRouter
from src.anisearch.data_models import Query
from src.anisearch.startup import services
from src.anisearch.endpoints import admin


router = APIRouter()
api_prefix = "/api/v1"

router.include_router(admin.router, tags=["Admin"], prefix=api_prefix)


@router.post("/api/v1/content", tags=["Content"])
async def get_relevant_content(query: Query):
    return await services.search_anime(query.text)


@router.get("/api/v1/content/{uid}", tags=["Content"])
def get_by_id(uid: int):
    return services.get_anime(uid)
