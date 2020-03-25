from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from _routes import set_routes
from _mongo import setup_mongo


app = FastAPI()
app.z = 1

app.mount("/static", StaticFiles(directory="templates"), name="static")

set_routes(app)
setup_mongo(app)
