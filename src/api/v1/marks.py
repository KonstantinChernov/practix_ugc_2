import logging

from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from auth_grpc.auth_check import check_permission
from db.models import Mark, AverageFilmRatingResponseModel, FilmMarksCountResponseModel
from exceptions import ObjectAlreadyExists, ObjectNotExists
from services.marks import FilmsService, get_films_service
from models.marks import BaseMark, MarkAction
from utils import get_user_login

router = APIRouter()

logging.basicConfig(level=logging.INFO)


@router.get(
    '/average-rating',
    summary='Точка для просмотра среднцей оценки фильма',
    description='Принимает id фильма',
    response_description='Возвращается средняя оценка фильма',
    tags=['marks'],
)
@check_permission(roles=['Subscriber'])
async def get_average_film_rating(
        data: BaseMark,
        film_service: FilmsService = Depends(get_films_service)
):
    average_rating = await film_service.get_average_rating(film_id=data.film_id)
    return AverageFilmRatingResponseModel(film_id=data.film_id, average_rating=average_rating)


@router.get(
    '/count',
    summary='Точка для просмотра количества оценок фильма',
    description='Принимает id фильма',
    response_description='Возвращается количество оценок фильма',
    tags=['marks'],
)
@check_permission(roles=['Subscriber'])
async def get_film_marks_count(
        data: BaseMark,
        film_service: FilmsService = Depends(get_films_service)
):
    marks_count = await film_service.get_marks_count(film_id=data.film_id)
    return FilmMarksCountResponseModel(film_id=data.film_id, marks_count=marks_count)


@router.delete(
    '/delete',
    summary='Точка для удаления оценки фильма',
    description='Принимает id фильма',
    response_description='Возвращается статус код 204',
    tags=['marks'],
)
@check_permission(roles=['Subscriber'])
async def delete_mark_from_film(
        request: Request,
        data: BaseMark,
        film_service: FilmsService = Depends(get_films_service)
):
    login = get_user_login(request)
    try:
        await film_service.delete_object(film_id=data.film_id, user_login=login)
    except ObjectNotExists:
        return JSONResponse(content={"type": "error", "message": "object doesn't exist"},
                            status_code=HTTPStatus.NOT_FOUND)
    return Response(status_code=HTTPStatus.NO_CONTENT)


@router.put(
    '/update',
    summary='Точка для обновления оценки фильма',
    description='Принимает id фильма и оценку новую оценку',
    response_description='Возвращается обновленная оценка',
    tags=['marks'],
)
@check_permission(roles=['Subscriber'])
async def update_mark_from_film(
    request: Request,
    data: MarkAction,
    film_service: FilmsService = Depends(get_films_service)
):
    login = get_user_login(request)
    try:
        Mark.check_mark(data.mark)
        await film_service.update_mark(film_id=data.film_id, user_login=login, mark_value=data.mark)
    except ObjectNotExists:
        return JSONResponse(content={"type": "error", "message": "object doesn't exist"},
                            status_code=HTTPStatus.NOT_FOUND)
    except ValueError:
        return JSONResponse(content={"type": "error", "message": "invalid mark value"},
                            status_code=HTTPStatus.BAD_REQUEST)
    return JSONResponse(content={"type": "success"},
                        status_code=HTTPStatus.OK)


@router.post(
    '/set',
    summary='Точка для добавления оценки фильму',
    description='Принимает id фильма и ',
    response_description='возвращается средняя оценка фильма',
    tags=['marks'],
)
@check_permission(roles=['Subscriber'])
async def set_mark_to_film(
    request: Request,
    data: MarkAction,
    film_service: FilmsService = Depends(get_films_service)
):
    login = get_user_login(request)
    try:
        mark = Mark(**data.dict(), user_login=login)
        await film_service.add_object(mark)
    except ObjectAlreadyExists:
        return JSONResponse(content={"type": "error", "message": "object already exist"},
                            status_code=HTTPStatus.BAD_REQUEST)
    except ValueError:
        return JSONResponse(content={"type": "error", "message": "invalid mark value"},
                            status_code=HTTPStatus.BAD_REQUEST)
    return JSONResponse(content={"type": "success", "data": jsonable_encoder(mark)},
                        status_code=HTTPStatus.CREATED)
