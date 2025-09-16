import logging
import fastapi
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

from settings import TEST_DATABASE_URL

app = fastapi.FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
        workers=1
    )
