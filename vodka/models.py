from motor.motor_asyncio import AsyncIOMotorDatabase

from settings import VODKA_COLLECTION
from common.models import BeerBlogItem


class Vodka(BeerBlogItem):

    def __init__(self, db: AsyncIOMotorDatabase, **kw):
        super().__init__(db)
        self.collection = self.db[VODKA_COLLECTION]
