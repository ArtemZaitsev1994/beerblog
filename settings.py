from os.path import isfile
from envparse import env
from envparse import ConfigurationError


BEER_COLLECTION = 'bb_beer'
NOT_CONFIRMED_QUESTION_COLLECTION = 'not_confirmed_quiz_questions'
ADMIN_COLLECTION = 'admin'

STATIC_PATH = '/static'

if isfile('.env'):
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
else:
    raise SystemExit('Create an env-file please.!')
