from fastapi import FastAPI
from app.db.base import init_models
from contextlib import asynccontextmanager
from app.routers import auth_router, note_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(note_router)
app.include_router(auth_router)
