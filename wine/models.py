from motor.motor_asyncio import AsyncIOMotorDatabase

from settings import WINE_COLLECTION
from common.models import Alcohol


class Wine(Alcohol):

    def __init__(self, db: AsyncIOMotorDatabase, **kw):
        super().__init__(db)
        self.collection = self.db[WINE_COLLECTION]
