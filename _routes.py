from collections import namedtuple
from fastapi.applications import FastAPI

from beer.views import router as beer_router
from common.views import router as common_router


Router = namedtuple('Router', ['router', 'prefix'])

routes = [
    Router(beer_router, '/beer'),
    Router(common_router, ''),
]


def set_routes(app: FastAPI):
    for route in routes:
        app.include_router(
            route.router,
            prefix=route.prefix,
        )
