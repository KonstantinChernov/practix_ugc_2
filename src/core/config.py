import os
from logging import config as logging_config

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies-ugc-2')


# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Auth host
AUTH_GRPC_HOST = os.getenv('AUTH_GRPC_HOST', '127.0.0.1')
AUTH_GRPC_PORT = os.getenv('AUTH_GRPC_PORT', '50051')


SENTRY_DSN = os.getenv('SENTRY_DSN')

MONGO_DETAILS = os.getenv('mongodb://localhost:27017')
MONGO_DB_NAME = 'ugc'
MONGO_MARK_COLLECTION_NAME = 'marks'
MONGO_FAVORITE_COLLECTION_NAME = 'favorites'
MONGO_REVIEW_COLLECTION_NAME = 'reviews'
MONGO_REVIEW_LIKES_COLLECTION_NAME = 'review_likes'
