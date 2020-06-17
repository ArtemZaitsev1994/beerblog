from motor import motor_asyncio as ma
from fastapi.applications import FastAPI

from settings import MONGO_DB_NAME, MONGO_HOST
from beer.models import Beer
from wine.models import Wine
from vodka.models import Vodka
from bar.models import Bar
from common.models import VersionModel


def setup_mongo(app: FastAPI):
    app.client = ma.AsyncIOMotorClient(MONGO_HOST)
    app.db = app.client[MONGO_DB_NAME]

    app.mongo = {
        'beer': Beer(app.db),
        'wine': Wine(app.db),
        'vodka': Vodka(app.db),
        'bar': Bar(app.db),
        'version': VersionModel(app.db)
    }
