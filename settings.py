import os

from fastapi.applications import FastAPI
from envparse import env


BEER_COLLECTION = 'beerblog_bb_beer'

STATIC_PATH = '/static'

BASEDIR = os.path.dirname(os.path.realpath(__file__))
PHOTO_PATH = os.path.join(BASEDIR, 'static/photo/')

if os.path.isfile('.env'):
    env.read_envfile('.env')

    # DEBUG = env.bool('DEBUG', default=False)

    MONGO_HOST = env.str('MONGO_HOST')
    MONGO_DB_NAME = env.str('MONGO_DB_NAME')

    # REDIS_HOST = env.tuple('REDIS_HOST')
    # SESSION_TTL = env.int('SESSION_TTL')

    # PORT = env.int('PORT')

    # try:
    #     ADMIN_LOGIN = env.str('ADMIN_LOGIN')
    #     ADMIN_PASSWORD = env.str('ADMIN_PASSWORD')
    # except ConfigurationError:
    #     ADMIN_PASSWORD, ADMIN_LOGIN = None, None

    JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')
    JWT_ALGORITHM = env.str('JWT_ALGORITHM')
    AUTH_SERVER_LINK = env.str('AUTH_SERVER_LINK')
else:
    raise SystemExit('Create an env-file please.!')


def setup_app(app: FastAPI):

    BASEDIR = os.path.dirname(os.path.realpath(__file__))
    PHOTO_PATH = os.path.join(BASEDIR, 'static/photo/')

    app.beer_photo_path = os.path.join(PHOTO_PATH, 'beer')
