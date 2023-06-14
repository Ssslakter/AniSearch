from pydantic import BaseModel


class AnimeData(BaseModel):
    """Dataclass for anime data"""

    uid: int
    title: str
    genres: list[str] | None
    aired: str | None
    episodes: int | None
    popularity: float | None
    score: float | None
    synopsis: str | None
    img_url: str | None
