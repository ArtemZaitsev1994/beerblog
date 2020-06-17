import os

from fastapi.applications import FastAPI
from envparse import env


if os.path.isfile('.env'):
    env.read_envfile('.env')
else:
    raise SystemExit('Create an env-file please.!')

MONGO_HOST = env.str('MONGO_HOST')
MONGO_DB_NAME = env.str('MONGO_DB_NAME')

JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')
JWT_ALGORITHM = env.str('JWT_ALGORITHM')
AUTH_SERVER_LINK = env.str('AUTH_SERVER_LINK')

BEER_COLLECTION = env.str('BEER_COLLECTION')
WINE_COLLECTION = env.str('WINE_COLLECTION')
VODKA_COLLECTION = env.str('VODKA_COLLECTION')
BAR_COLLECTION = env.str('BAR_COLLECTION')
VERSION_COLLECTION = env.str('VERSION_COLLECTION')


def setup_app(app: FastAPI):

    BASEDIR = os.path.dirname(os.path.realpath(__file__))
    PHOTO_PATH = os.path.join(BASEDIR, 'photo/')

    app.photo_path = {
        'beer': os.path.join(PHOTO_PATH, 'beer'),
        'wine': os.path.join(PHOTO_PATH, 'wine'),
        'vodka': os.path.join(PHOTO_PATH, 'vodka'),
        'bar': os.path.join(PHOTO_PATH, 'bar'),
    }

    app.version = '0.0.1'


async def check_version(app: FastAPI):
    version = await app.mongo['version'].get_current_version()
    if version is None:
        await app.mongo['version'].set_current('0.0.1')
