from motor.motor_asyncio import AsyncIOMotorDatabase

from settings import BAR_COLLECTION
from common.models import BeerBlogItem


class Bar(BeerBlogItem):
    """Бары, сами по себе, отзыв о баре в котором был"""

    def __init__(self, db: AsyncIOMotorDatabase, **kw):
        super().__init__(db)
        self.collection = self.db[BAR_COLLECTION]
