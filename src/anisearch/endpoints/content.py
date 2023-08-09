from fastapi import APIRouter
from src.anisearch.data_models import Query, UserQuery
from src.anisearch.startup import services


router = APIRouter(
    prefix="/content",
    responses={404: {"description": "Not found"}},
)


@router.post("", tags=["Content"])
async def get_relevant_content(query: Query):
    docs = await services.search_anime(query.text)
    return docs[: services.OUTPUT_AMOUNT]


@router.get("/{uid}", tags=["Content"])
def get_by_id(uid: int):
    return services.get_anime(uid)


@router.post("/recommend", tags=["Content"])
async def get_relevant_for_user(query: UserQuery):
    return (await services.recommend_from_relevant(query.nickname, query.text))[
        : services.OUTPUT_AMOUNT
    ]


@router.post("/text_search", tags=["Content"])
async def get_relevant_text_search(query: Query):
    docs = await services.full_search(query.text)
    return docs[: services.OUTPUT_AMOUNT]


@router.get("/recommend/{nickname}", tags=["Content"])
def get_by_user(nickname: str):
    return services.recommend_anime(nickname)
