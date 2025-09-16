from decouple import config

from sqlalchemy import URL

DEBUG = config("DEBUG", cast=bool, default=True)

SECRET = config('SECRET', default='testkey')


POSTGRES_ENGINE = "postgresql+asyncpg"
POSTGRES_HOST = config('POSTGRES_HOST', default='localhost')
POSTGRES_DB = config('POSTGRES_DB') 
POSTGRES_PORT = config('POSTGRES_PORT')
POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')

# DATABASE_URL = f"{POSTGRES_ENGINE}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

DATABASE_URL = URL.create(
    drivername=POSTGRES_ENGINE,
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB
)

POSTGRES_TEST_ENGINE = "postgresql+psycopg2"

POSTGRES_TEST_HOST = config('POSTGRES_TEST_HOST', default='localhost')
POSTGRES_TEST_DB = config('POSTGRES_TEST_DB') 
POSTGRES_TEST_PORT = config('POSTGRES_TEST_PORT')
POSTGRES_TEST_USER = config('POSTGRES_TEST_USER')
POSTGRES_TEST_PASSWORD = config('POSTGRES_TEST_PASSWORD')


TEST_DATABASE_URL = URL.create(
    drivername=POSTGRES_TEST_ENGINE,
    username=POSTGRES_TEST_USER,
    password=POSTGRES_TEST_PASSWORD,
    host=POSTGRES_TEST_HOST,
    port=POSTGRES_TEST_PORT,
    database=POSTGRES_TEST_DB
)


