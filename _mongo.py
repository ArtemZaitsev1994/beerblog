import json
from motor import motor_asyncio as ma
from fastapi.applications import FastAPI

from settings import MONGO_DB_NAME, MONGO_HOST
from beer.models import Beer


def setup_mongo(app: FastAPI):
    app.client = ma.AsyncIOMotorClient(MONGO_HOST)
    app.db = app.client[MONGO_DB_NAME]

    app.mongo = {
        'beer': Beer(app.db),
    }

    # app.on_startup.append(_check_admin)
    # app.on_startup.append(fill_db)


# async def fill_db(app: Application):
#     qs, _ = await app['models']['questions'].get_part(None, 10)
#     if len(qs) > 0:
#         return

#     async with AIOFile('questions.json', 'r') as f:
#         questions = json.loads(await f.read())

#     await app['models']['questions'].add_questions_many(questions)
