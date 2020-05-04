from collections import namedtuple
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from beer.views import router as beer_router
from wine.views import router as wine_router
from vodka.views import router as vodka_router
from common.views import router as common_router


templates = Jinja2Templates(directory="templates")


Router = namedtuple('Router', ['router', 'prefix'])

routes = [
    Router(beer_router, '/beer'),
    Router(wine_router, '/wine'),
    Router(vodka_router, '/vodka'),
    Router(common_router, ''),
]


def set_routes(app: FastAPI):
    for route in routes:
        app.include_router(
            route.router,
            prefix=route.prefix,
        )

    app.mount("/templates", StaticFiles(directory="templates/"), name="templates")
    app.mount("/css", StaticFiles(directory="templates/css"), name="css")
    app.mount("/js", StaticFiles(directory="templates/js"), name="js")
    app.mount("/photo", StaticFiles(directory="static/photo"), name="photo")
    app.mount("/static", StaticFiles(directory="static/"), name="static")

    @app.exception_handler(StarletteHTTPException)
    async def http_not_found_handler(request: Request, exc: Exception):
        return templates.TemplateResponse("404.html", {"request": request})
