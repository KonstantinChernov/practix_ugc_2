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


class Mark(BaseModel):
    film_id: uuid.UUID
    mark: int
    datetime: Optional[datetime]

    @validator('datetime', pre=True, always=True)
    def set_datetime_now(cls, v):
        return v or datetime.now()


@router.post(
    '',
    summary='Точка сбора информации об оценках',
    description='Принимает id фильма и оценку пользователя',
    response_description='возвращается статус код',
    tags=['marks'],
)
# @check_permission(roles=['Subscriber'])
async def collect_mark(
    request: Request,
    mark: Mark,
):
    token = request.headers.get('Authorization', None)
    token = token.replace('Bearer ', '')
    decoded_token = jwt.decode(token, options={'verify_signature': False})
    login = decoded_token.get('sub', None)

    return {'login': login, **mark.dict()}


