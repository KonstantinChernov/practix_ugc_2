import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from auth_grpc.auth_check import check_permission
from exceptions import ForbiddenError, ObjectAlreadyExists, ObjectNotExists
from models.reviews import Review, ReviewIn, ReviewsGetIn
from services.reviews import ReviewService, get_review_service
from utils import get_user_login

router = APIRouter()

logging.basicConfig(level=logging.INFO)


@router.post(
    '/add',
    summary='Точка для добавления рецензии к фильму',
    description='Принимает id фильма и текст рецензии',
    response_description='Возвращется добавленная рецензия',
    tags=['reviews'],
)
@check_permission(roles=['Subscriber'])
async def add_reviews(
        request: Request,
        data: ReviewIn,
        review_service: ReviewService = Depends(get_review_service)):
    login = get_user_login(request)
    try:
        review = Review(**data.dict(), user_login=login)
        await review_service.add_object(review)
    except ObjectAlreadyExists:
        return JSONResponse(content={"type": "error", "message": "object already exist"},
                            status_code=HTTPStatus.BAD_REQUEST)

    return JSONResponse(content={"type": "success", "data": jsonable_encoder(review, exclude_none=True)},
                        status_code=HTTPStatus.CREATED)


@router.delete(
    '/delete/{review_id}',
    summary='Точка для удаления рецензии пользователя для фильма',
    description='Принимает id рецензии и id фильма',
    response_description='Возвращается статус код 204',
    tags=['reviews'],
)
@check_permission(roles=['Subscriber'])
async def delete_review(
        request: Request,
        review_id: str,
        review_service: ReviewService = Depends(get_review_service)
):
    login = get_user_login(request)
    try:
        await review_service.delete_object(_id=review_id, user_login=login)
    except ObjectNotExists:
        return JSONResponse(content={"type": "error", "message": "object doesn't exist"},
                            status_code=HTTPStatus.NOT_FOUND)
    except ForbiddenError:
        return JSONResponse(content={"type": "error", "message": "access denied"},
                            status_code=HTTPStatus.FORBIDDEN)
    return Response(status_code=HTTPStatus.NO_CONTENT)


@router.post(
    '/set-like/{review_id}',
    summary='Точка для лайка/дизлайка рецензии к фильму',
    description='Принимает id рецензии',
    response_description='Возвращется статус 200',
    tags=['reviews'],
)
@check_permission(roles=['Subscriber'])
async def set_like(
        request: Request,
        review_id: str,
        review_service: ReviewService = Depends(get_review_service)):
    login = get_user_login(request)
    try:
        await review_service.set_like_to_review(review_id=review_id, user_login=login)
    except ObjectNotExists:
        return JSONResponse(content={"type": "error", "message": "object doesn't exist"},
                            status_code=HTTPStatus.NOT_FOUND)
    return JSONResponse(content={"type": "success"},
                        status_code=HTTPStatus.OK)


@router.get(
    '',
    summary='Точка для получения рецензий фильма',
    response_description='Возвращется список рецензий',
    tags=['reviews'],
)
@check_permission(roles=['Subscriber'])
async def get_reviews(
        data: ReviewsGetIn,
        review_service: ReviewService = Depends(get_review_service),

):
    reviews = await review_service.get_objects(film_id=data.film_id)
    return JSONResponse(content={"type": "success", "data": jsonable_encoder(reviews)},
                        status_code=HTTPStatus.OK)
