import uuid
from typing import Any

from pydantic import BaseModel


class FavouriteIn(BaseModel):
    film_id: uuid.UUID


class Favorite(BaseModel):
    id: Any
    film_id: uuid.UUID
    user_login: str
