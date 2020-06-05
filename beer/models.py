from motor.motor_asyncio import AsyncIOMotorDatabase

from settings import BEER_COLLECTION
from common.models import BeerBlogItem


class Beer(BeerBlogItem):

    def __init__(self, db: AsyncIOMotorDatabase, **kw):
        super().__init__(db)
        self.collection = self.db[BEER_COLLECTION]
