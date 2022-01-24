import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import validator

from utils import CustomBaseModel


class ReviewIn(CustomBaseModel):
    film_id: uuid.UUID
    review: str


class Review(CustomBaseModel):
    id: Any
    film_id: uuid.UUID
    review: str
    datetime: Optional[datetime]
    user_login: str
    likes: Optional[int]

    @validator('datetime', pre=True, always=True)
    def set_datetime_now(cls, v):
        return v or datetime.now()


class ReviewLike(CustomBaseModel):
    review_id: str
    user_login: str


class ReviewLikeIn(CustomBaseModel):
    film_id: uuid.UUID
    user_login: str


class ReviewsGetIn(CustomBaseModel):
    film_id: uuid.UUID
