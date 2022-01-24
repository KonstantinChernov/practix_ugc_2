import uuid
from typing import Any

from utils import CustomBaseModel


class FavouriteIn(CustomBaseModel):
    film_id: uuid.UUID


class Favorite(CustomBaseModel):
    id: Any
    film_id: uuid.UUID
    user_login: str
