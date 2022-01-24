from typing import Any

from bson import ObjectId

from db.mongodb import AbstractDBAdapter
from exceptions import ObjectAlreadyExists, ObjectNotExists, ForbiddenError


class BaseService:

    def __init__(self,
                 db_adapter: AbstractDBAdapter,
                 collection_name: str,
                 model: Any):
        self.db_adapter = db_adapter
        self.model = model
        self.collection_name = collection_name

    async def get_objects(self, count: int = 15, page: int = 1, **kwargs):
        objects = await self.db_adapter.get_objects_from_db(self.model,
                                                            kwargs,
                                                            self.collection_name)
        return objects[count * (page - 1):count * page]

    async def add_object(self, obj: Any):
        already_exists_object = await self.db_adapter.get_object_from_db(self.model,
                                                                         {'film_id': obj.film_id,
                                                                          'user_login': obj.user_login},
                                                                         self.collection_name)
        if already_exists_object:
            raise ObjectAlreadyExists()
        await self.db_adapter.add_object_to_db(obj.dict(exclude_none=True), self.collection_name)

    async def delete_object(self, **kwargs):
        if kwargs.get('_id'):
            kwargs['_id'] = ObjectId(kwargs['_id'])
        exist_obj = await self.db_adapter.get_object_from_db(self.model,
                                                             kwargs,
                                                             self.collection_name)
        if not exist_obj:
            raise ObjectNotExists()
        if exist_obj.user_login != kwargs['user_login']:
            raise ForbiddenError()
        await self.db_adapter.delete_object_from_db(kwargs,
                                                    self.collection_name)
