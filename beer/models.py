from typing import Dict, List, Any

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from settings import BEER_COLLECTION


class Alcohol:

    def __init__(self, db: AsyncIOMotorDatabase, **kw):
        self.db = db
        self.collection = NotImplementedError

    async def get_all(self, page=1, per_page=9) -> List[Dict[str, Any]]:
        all_qs = self.collection.find()
        count_qs = await self.collection.count_documents({})
        has_next = count_qs > per_page * page
        qs = await all_qs.skip((page - 1) * per_page).limit(per_page).to_list(length=None)

        pagination = {
            'has_next': has_next,
            'prev': page - 1 if page > 1 else None,
            'next': page + 1 if has_next else None,
            'page': page,
            'per_page': per_page,
            'max': count_qs // per_page if count_qs % per_page == 0 else count_qs // per_page + 1
        }

        return qs, pagination

    async def get_all_documents(self):
        return await self.collection.find().to_list(length=None)

    async def insert_item(self, data):
        print(data)
        return await self.collection.insert_one(data)

    async def clear_db(self):
        await self.collection.drop()


class Beer(Alcohol):

    def __init__(self, db: AsyncIOMotorDatabase, **kw):
        super().__init__(db)
        self.collection = self.db[BEER_COLLECTION]
