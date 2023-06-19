from fastapi import APIRouter
from src.anisearch.startup import services
from src.anisearch.data_models import AnimeData


router = APIRouter(
    prefix="/admin",
    responses={404: {"description": "Not found"}},
)


@router.post("/content")
async def add_content(anime_data: AnimeData):
    return services.insert_anime(anime_data)


@router.delete("/content/{uid}")
async def delete_content(uid: int):
    return services.delete_anime(uid)


@router.get("/qdrant")
async def get_collections():
    return services.get_collections()
