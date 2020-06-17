from fastapi import FastAPI

from _routes import set_routes
from _mongo import setup_mongo
from settings import setup_app, check_version
from common.middlewares import CheckUserAuthMiddleware


app = FastAPI()

setup_app(app)
setup_mongo(app)
set_routes(app)

app.add_middleware(CheckUserAuthMiddleware)


@app.on_event('startup')
async def startup():
    await check_version(app)
