from pydantic import BaseModel, Field, validator, ValidationError
import uuid
from typing import Optional
from datetime import datetime


class Review(BaseModel):
    film_id: uuid.UUID
    review: str
    datetime: Optional[datetime]

    @validator('datetime', pre=True, always=True)
    def set_datetime_now(cls, v):
        return v or datetime.now()


class Favourite(BaseModel):
    film_id: uuid.UUID


class Mark(BaseModel):
    film_id: Optional[uuid.UUID]
    mark: int
    datetime: Optional[datetime]
    user_login: Optional[str]

    @validator('datetime', pre=True, always=True)
    def set_datetime_now(cls, v):
        if not v:
            return datetime.now()
        return v

    @validator('mark', pre=True, always=True)
    def check_mark(cls, v):
        if v > 10 or v < 1:
            raise ValueError('Invalid value for mark field')
        return v

mark = Mark(film_id='0253a065-a55f-4984-b99a-3b0619678478', mark=9, user_login='fdsafds')


class AverageFilmRatingResponseModel(BaseModel):
    film_id: uuid.UUID
    average_rating: float


class FilmMarksCountResponseModel(BaseModel):
    film_id: uuid.UUID
    marks_count: int
