from pydantic import BaseModel
import uuid
from typing import Any


class FavouriteIn(BaseModel):
    film_id: uuid.UUID


class Favorite(BaseModel):
    id: Any
    film_id: uuid.UUID
    user_login: str



