import logging
import uuid
from datetime import datetime
from http import HTTPStatus
from typing import Optional

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field, validator

from auth_grpc.auth_check import check_permission

router = APIRouter()

logging.basicConfig(level=logging.INFO)


class Review(BaseModel):
    film_id: uuid.UUID
    review: str
    datetime: Optional[datetime]

    @validator('datetime', pre=True, always=True)
    def set_datetime_now(cls, v):
        return v or datetime.now()


@router.post(
    '',
    summary='Точка сбора информации о рецензиях',
    description='Принимает id фильма и рецензию пользователя',
    response_description='возвращается статус код',
    tags=['reviews'],
)
# @check_permission(roles=['Subscriber'])
async def collect_review(
    request: Request,
    review: Review,
):

    token = request.headers.get('Authorization', None)
    token = token.replace('Bearer ', '')
    decoded_token = jwt.decode(token, options={'verify_signature': False})
    login = decoded_token.get('sub', None)

    return {'login': login, **review.dict()}


