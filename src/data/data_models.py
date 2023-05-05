from dataclasses import dataclass


@dataclass
class AnimeRating:
    """Class representing rating that user gives to the anime
    """
    anime_id: str
    user_link: str
    rating: int | None

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not 1 <= value <= 10:
            raise ValueError("Rating must be between 1 and 90.")
        self._rating = value
