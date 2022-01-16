from functools import lru_cache

from fastapi import Depends

from db.mongodb import get_mongo, AbstractDBAdapter
from models.favorites import Favorite
from services.base_services.object_service import BaseService
from core.config import MONGO_FAVORITE_COLLECTION_NAME


class FavoritesService(BaseService):
    pass


@lru_cache()
def get_favorite_service(
        db_adapter: AbstractDBAdapter = Depends(get_mongo),
) -> FavoritesService:
    return FavoritesService(db_adapter=db_adapter,
                            model=Favorite,
                            collection_name=MONGO_FAVORITE_COLLECTION_NAME)

