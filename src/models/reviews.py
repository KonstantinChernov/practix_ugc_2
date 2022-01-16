from pydantic import BaseModel, validator
import uuid
from typing import Optional, Any
from datetime import datetime


class ReviewIn(BaseModel):
    film_id: uuid.UUID
    review: str


class Review(BaseModel):
    id: Any
    film_id: uuid.UUID
    review: str
    datetime: Optional[datetime]
    user_login: str
    likes: Optional[int]

    @validator('datetime', pre=True, always=True)
    def set_datetime_now(cls, v):
        return v or datetime.now()


class ReviewLike(BaseModel):
    review_id: str
    user_login: str


class ReviewLikeIn(BaseModel):
    film_id: uuid.UUID
    user_login: str


class ReviewsGetIn(BaseModel):
    film_id: uuid.UUID
