from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.db import create_tables
from uvicorn import run
from api.users import router as user_router


@asynccontextmanager
async def lifespan(app):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(user_router)
# app.include_router()


if __name__ == "__main__":
    run(app)
