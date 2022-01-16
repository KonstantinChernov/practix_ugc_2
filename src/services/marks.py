import uuid
from functools import lru_cache

from fastapi import Depends

from core.config import MONGO_MARK_COLLECTION_NAME
from db.models import Mark
from db.mongodb import AbstractDBAdapter, get_mongo
from exceptions import ObjectNotExists
from services.base_services.object_service import BaseService


class FilmsService(BaseService):

    async def get_average_rating(self, film_id: uuid.UUID):
        query = {'film_id': film_id}
        films = await self.db_adapter.get_objects_from_db(Mark, query, self.collection_name)
        average_rating = sum([film.mark for film in films]) / len(films)
        return average_rating

    async def get_marks_count(self, film_id: uuid.UUID):
        query = {'film_id': film_id}
        films = await self.db_adapter.get_objects_from_db(Mark, query, self.collection_name)
        return len(films)

    async def update_mark(self, user_login: str, film_id: uuid.UUID, mark_value: int):
        mark = await self.db_adapter.get_object_from_db(Mark,
                                                        {'film_id': film_id, 'user_login': user_login},
                                                        self.collection_name)
        if not mark:
            raise ObjectNotExists()
        await self.db_adapter.update_object_from_db({'film_id': mark.film_id, 'user_login': mark.user_login},
                                                    {'$set': {'mark': mark_value}},
                                                    self.collection_name)


@lru_cache()
def get_films_service(
        db_adapter: AbstractDBAdapter = Depends(get_mongo),
) -> FilmsService:
    return FilmsService(db_adapter=db_adapter,
                        model=Mark,
                        collection_name=MONGO_MARK_COLLECTION_NAME)
