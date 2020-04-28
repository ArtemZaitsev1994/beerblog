from motor.motor_asyncio import AsyncIOMotorDatabase

from settings import BEER_COLLECTION
from common.models import Alcohol


class Beer(Alcohol):

    def __init__(self, db: AsyncIOMotorDatabase, **kw):
        super().__init__(db)
        self.collection = self.db[BEER_COLLECTION]
