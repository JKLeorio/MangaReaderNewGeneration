import logging
import fastapi
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

from settings import TEST_DATABASE_URL

from api.auth import (
    auth_router,
    register_router
    )
from api.manga import (
    comic_router,
    page_router,
    chapter_router
)
from api.person import person_router
from api.media import media_router

app = fastapi.FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)
app.include_router(
    register_router,
    prefix="/register",
    tags=["Register"]
)
app.include_router(
    comic_router,
    prefix="/comics",
    tags=["Comics"]
)
app.include_router(
    chapter_router,
    prefix="/chapters",
    tags=["Chaptes"]
)
app.include_router(
    page_router,
    prefix="/pages",
    tags=["Pages"]
)
app.include_router(
    person_router,
    prefix="/persons",
    tags=["Persons"]
)
app.include_router(
    media_router,
    prefix="/media",
    tags=["Media"]
)


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=8000,
        workers=1
    )
