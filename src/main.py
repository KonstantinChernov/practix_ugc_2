import logging

import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from api.v1 import favourites, marks, reviews
from core import config
from db import mongodb
from tracer import tracer

app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    title='UGC API для онлайн-кинотеатра',
    description='Сервис для работы с данными для аналитики Онлайн-кинотеатра',
    version='1.0.0',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    mongodb.mongo_client = AsyncIOMotorClient(config.MONGO_DETAILS)


sentry_sdk.init(dsn=config.SENTRY_DSN)

app.logger = logging.getLogger(__name__)
app.logger.setLevel(logging.INFO)


@app.middleware('http')
async def add_tracing(request: Request, call_next):
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is required')
    response = await call_next(request)
    with tracer.start_span(request.url.path) as span:
        request_id = request.headers.get('X-Request-Id')
        span.set_tag('http.request_id', request_id)
        span.set_tag('http.url', request.url)
        span.set_tag('http.method', request.method)
        span.set_tag('http.status_code', response.status_code)
    return response


app.include_router(marks.router, prefix='/api/v1/marks', tags=['marks'])
app.include_router(reviews.router, prefix='/api/v1/reviews', tags=['reviews'])
app.include_router(favourites.router, prefix='/api/v1/favourites', tags=['favourites'])

app.add_middleware(SentryAsgiMiddleware)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
