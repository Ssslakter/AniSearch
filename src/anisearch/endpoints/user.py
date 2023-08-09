import pandas as pd
from fastapi import APIRouter
from src.anisearch.data_models import Query, UserQuery
from src.anisearch.startup import services


router = APIRouter(
    prefix="/user",
    responses={404: {"description": "Not found"}},
)

df = pd.read_csv("data/external/reviews.csv").groupby(["profile"]).count()["uid"].sort_values().iloc[::-1]
users = df.keys().tolist()


@router.get("/all/{page}", tags=["User"])
async def get_users(page: int):
    page_size = 50
    return users[page * page_size:][0:page_size]
