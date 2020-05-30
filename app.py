from fastapi import FastAPI

from _routes import set_routes
from _mongo import setup_mongo
from _elasticsearch import setup_es
from settings import setup_app
from common.middlewares import CheckUserAuthMiddleware


app = FastAPI()


@app.on_event('startup')
async def startup():
    set_routes(app)
    setup_mongo(app)
    setup_app(app)
    # await setup_es(app)

app.add_middleware(CheckUserAuthMiddleware)
