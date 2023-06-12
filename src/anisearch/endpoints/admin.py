from fastapi import APIRouter
from src.anisearch.startup import services
from src.anisearch.data_models import AnimeData


router = APIRouter(
    prefix="/admin",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/content")
async def add_anime(anime_data: AnimeData):
    return services.insert_anime(anime_data)


@router.get("/qdrant")
async def check_storage():
    return services.get_collections()
