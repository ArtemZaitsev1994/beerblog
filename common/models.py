from typing import Dict, List, Any
import datetime

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import DESCENDING


class BeerBlogItem:

    def __init__(self, db: AsyncIOMotorDatabase, **kw):
        self.db = db
        self.collection = NotImplementedError

    async def get_all(
        self,
        query: str = '',
        page: int = 1,
        sorting: tuple = ('_id', DESCENDING),
        per_page: int = 9
    ) -> List[Dict[str, Any]]:
        query_filter = {'search_by_name': {'$regex': f'.*{query.lower()}.*'}, 'not_confirmed': None}
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
        data['comments'] = []
        return await self.collection.insert_one(data)

    async def clear_db(self):
        await self.collection.drop()

    async def add_comment(self, _id: str, comment: Dict[str, str]):
        t = datetime.datetime.now()
        months = {
            1: 'янв',
            2: 'фев',
            3: 'мар',
            4: 'апр',
            5: 'май',
            6: 'июн',
            7: 'июл',
            8: 'авг',
            9: 'сен',
            10: 'окт',
            11: 'ноя',
            12: 'дек',
        }
        comment['date'] = f'{t.day} {months[t.month]} {t.year} в {t.hour}:{t.minute}'
        return await self.collection.update_one({'_id': ObjectId(_id)}, {'$push': {'comments': comment}})

    async def update_rate(self, _id: str, rate: int, login: str):
        item = await self.collection.find_one({'_id': ObjectId(_id)})
        rates = item['rates']
        rates[login] = rate
        sum_rate_nums = sum([x for x in rates.values()])
        new_rate = sum_rate_nums / len(item['rates'])
        new_rate = round(new_rate)

        result = await self.collection.update_one(
            {'_id': ObjectId(_id)},
            {'$set': {f'rates.{login}': rate, 'rate': new_rate}}
        )
        return result, new_rate

    # ---- Adminka ----- #

    async def count_not_confirmed(self):
        return await self.collection.count_documents({'not_confirmed': True})

    async def count_all(self):
        return await self.collection.count_documents({})

    async def get_items_admin(
        self,
        query: str = '',
        page: int = 1,
        sorting: tuple = ('_id', DESCENDING),
        per_page: int = 9,
        not_confirmed: bool = None,
    ) -> List[Dict[str, Any]]:
        query_filter = {
            'search_by_name': {'$regex': f'.*{query.lower()}.*'},
        }
        if not_confirmed is not None:
            query_filter['not_confirmed'] = not_confirmed if not_confirmed else None

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

    async def change_item_state(self, _id: str, not_confirmed: bool):
        value = True if not_confirmed else None

        result = await self.collection.update_one(
            {'_id': ObjectId(_id)},
            {'$set': {'not_confirmed': value}}
        )
        return result

    async def delete_item(self, _id: str):
        return await self.collection.delete_one({'_id': ObjectId(_id)})
