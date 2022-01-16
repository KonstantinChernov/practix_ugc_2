import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from auth_grpc.auth_check import check_permission
from models.favorites import Favorite, FavouriteIn
from exceptions import ObjectAlreadyExists, ObjectNotExists, ForbiddenError
from services.favourites import FavoritesService, get_favorite_service
from utils import get_user_login

router = APIRouter()

logging.basicConfig(level=logging.INFO)


@router.get(
    '',
    summary='Точка для просмотра закладок пользователя',
    response_description='Возвращется список закладок',
    tags=['favorites'],
)
@check_permission(roles=['Subscriber'])
async def get_favorites(
        request: Request,
        favorite_service: FavoritesService = Depends(get_favorite_service)
):
    login = get_user_login(request)
    favorites = await favorite_service.get_objects(user_login=login)
    return JSONResponse(content={"type": "success", "data": jsonable_encoder(favorites)},
                        status_code=HTTPStatus.OK)


@router.post(
    '/add',
    summary='Точка для добавления фильма в закладку',
    description='Принимает id фильма',
    response_description='Возвращается созданную закладку',
    tags=['favorites'],
)
@check_permission(roles=['Subscriber'])
async def add_favorites(
        request: Request,
        data: FavouriteIn,
        favorite_service: FavoritesService = Depends(get_favorite_service)
):
    login = get_user_login(request)
    favorite = Favorite(user_login=login, film_id=data.film_id)
    try:
        await favorite_service.add_object(favorite)
    except ObjectAlreadyExists:
        return JSONResponse(content={"type": "error", "message": "object already exist"},
                            status_code=HTTPStatus.BAD_REQUEST)
    return JSONResponse(content={"type": "success", "data": jsonable_encoder(favorite, exclude_none=True)},
                        status_code=HTTPStatus.CREATED)


@router.delete(
    '/delete/{favorite_id}',
    summary='Точка для удаления закладки фильа',
    description='Принимает id закладки',
    response_description='Возвращается статус код 204',
    tags=['favorites'],
)
@check_permission(roles=['Subscriber'])
async def delete_favorite(
        request: Request,
        favorite_id: str,
        favorite_service: FavoritesService = Depends(get_favorite_service)
):
    login = get_user_login(request)
    try:
        await favorite_service.delete_object(_id=favorite_id, user_login=login)
    except ObjectNotExists:
        return JSONResponse(content={"type": "error", "message": "object doesn't exist"},
                            status_code=HTTPStatus.NOT_FOUND)
    except ForbiddenError:
        return JSONResponse(content={"type": "error", "message": "access denied"},
                            status_code=HTTPStatus.FORBIDDEN)
    return Response(status_code=HTTPStatus.NO_CONTENT)
