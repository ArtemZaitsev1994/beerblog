from typing import Dict, List, Any

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import DESCENDING


class Alcohol:

    def __init__(self, db: AsyncIOMotorDatabase, **kw):
        self.db = db
        self.collection = NotImplementedError

    async def get_all(
        self,
        page: int = 1,
        sorting: tuple = ('_id', DESCENDING),
        per_page: int = 9
    ) -> List[Dict[str, Any]]:
        query_filter = {'not_confirmed': None}
        all_qs = self.collection.find(query_filter)
        count_qs = await self.collection.count_documents(query_filter)
        has_next = count_qs > per_page * page
        qs = await all_qs.sort(*sorting).skip((page - 1) * per_page).limit(per_page).to_list(length=None)

        pagination = {
            'has_next': has_next,
            'prev': page - 1 if page > 1 else None,
            'next': page + 1 if has_next else None,
            'page': page,
            'per_page': per_page,
            'max': count_qs // per_page if count_qs % per_page == 0 else count_qs // per_page + 1
        }

        return qs, pagination

    async def get_item(self, _id: str) -> Dict[str, Any]:
        return await self.collection.find_one({'_id': ObjectId(_id)})

    async def get_all_documents(self):
        return await self.collection.find().to_list(length=None)

    async def insert_item(self, data):
        data['not_confirmed'] = True
        return await self.collection.insert_one(data)

    async def clear_db(self):
        await self.collection.drop()
