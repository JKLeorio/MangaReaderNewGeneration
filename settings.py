from datetime import timedelta
from decouple import config

from sqlalchemy import URL

#Debug mode for development
DEBUG: str = config("DEBUG", cast=bool, default=True)

#secret key for authorization system and other
SECRET: str = config('SECRET', default='testkey')

#database enviroment
POSTGRES_ENGINE = "postgresql+asyncpg"
POSTGRES_HOST: str = config('POSTGRES_HOST', default='localhost')
POSTGRES_DB: str = config('POSTGRES_DB') 
POSTGRES_PORT: str = config('POSTGRES_PORT')
POSTGRES_USER: str = config('POSTGRES_USER')
POSTGRES_PASSWORD: str = config('POSTGRES_PASSWORD')

DATABASE_URL: URL = URL.create(
    drivername=POSTGRES_ENGINE,
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB
)

#database enviroment for test
POSTGRES_TEST_ENGINE = "postgresql+psycopg2"

POSTGRES_TEST_HOST: str = config('POSTGRES_TEST_HOST', default='localhost')
POSTGRES_TEST_DB: str = config('POSTGRES_TEST_DB') 
POSTGRES_TEST_PORT: str = config('POSTGRES_TEST_PORT')
POSTGRES_TEST_USER: str = config('POSTGRES_TEST_USER')
POSTGRES_TEST_PASSWORD: str = config('POSTGRES_TEST_PASSWORD')

TEST_DATABASE_URL: URL = URL.create(
    drivername=POSTGRES_TEST_ENGINE,
    username=POSTGRES_TEST_USER,
    password=POSTGRES_TEST_PASSWORD,
    host=POSTGRES_TEST_HOST,
    port=POSTGRES_TEST_PORT,
    database=POSTGRES_TEST_DB
)

#Jwt token lifetime
TOKEN_LIFETIME = timedelta(days=1)

TOKEN_ALGORITHM = "HS256"


SUPPORTED_IMAGE_EXTENSIONS = [
    "jpg",
    "jpeg",
    "png"
]


MEDIA = "/media/"
