import uuid
from functools import lru_cache

from bson import ObjectId
from fastapi import Depends

from core.config import MONGO_REVIEW_COLLECTION_NAME, MONGO_REVIEW_LIKES_COLLECTION_NAME
from db.mongodb import AbstractDBAdapter, get_mongo
from exceptions import ObjectNotExists
from models.reviews import Review, ReviewLike
from services.base_services.object_service import BaseService


class ReviewService(BaseService):
    async def set_like_to_review(self, review_id: str, user_login: str):
        exist_review = await self.db_adapter.get_object_from_db(
            self.model, {'_id': ObjectId(review_id)}, self.collection_name
        )
        if not exist_review:
            raise ObjectNotExists()
        already_exists_like = await self.db_adapter.get_object_from_db(
            ReviewLike,
            {'review_id': review_id, 'user_login': user_login},
            MONGO_REVIEW_LIKES_COLLECTION_NAME,
        )
        if already_exists_like:
            return await self.db_adapter.delete_object_from_db(
                {'review_id': review_id, 'user_login': user_login},
                MONGO_REVIEW_LIKES_COLLECTION_NAME,
            )

        await self.db_adapter.add_object_to_db(
            {'review_id': review_id, 'user_login': user_login},
            MONGO_REVIEW_LIKES_COLLECTION_NAME,
        )

    async def get_objects(self, count: int = 15, page: int = 1, **kwargs):
        film_reviews = await self.db_adapter.get_objects_from_db(
            self.model, {'film_id': kwargs['film_id']}, self.collection_name
        )
        if film_reviews:
            for review in film_reviews:
                likes = await self.db_adapter.get_objects_from_db(
                    self.model,
                    {'review_id': ObjectId(review.id)},
                    MONGO_REVIEW_LIKES_COLLECTION_NAME,
                )
                review.likes = len(likes)
        return film_reviews


@lru_cache()
def get_review_service(
    db_adapter: AbstractDBAdapter = Depends(get_mongo),
) -> ReviewService:
    return ReviewService(
        db_adapter=db_adapter,
        model=Review,
        collection_name=MONGO_REVIEW_COLLECTION_NAME,
    )
