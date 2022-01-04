import logging
import uuid
from datetime import datetime
from http import HTTPStatus

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from auth_grpc.auth_check import check_permission

router = APIRouter()

logging.basicConfig(level=logging.INFO)


class Favourite(BaseModel):
    film_id: uuid.UUID


@router.post(
    '',
    summary='Точка сбора информации о закладках',
    description='Принимает id фильма для закладки пользователя',
    response_description='возвращается статус код',
    tags=['favourites'],
)
# @check_permission(roles=['Subscriber'])
async def collect_review(
    request: Request,
    favourite: Favourite,
):

    token = request.headers.get('Authorization', None)
    token = token.replace('Bearer ', '')
    decoded_token = jwt.decode(token, options={'verify_signature': False})
    login = decoded_token.get('sub', None)

    return {'login': login, **favourite.dict()}


