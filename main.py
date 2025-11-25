from contextlib import asynccontextmanager
import uvicorn
from fastapi import Body, Depends, FastAPI, status, Path
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.notes import Note
from settings import get_db, api_config
from handlers.notes import router as notes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    app.state.redis = api_config.redis_client()
    if not await app.state.redis.ping(): # type: ignore
        raise ConnectionError("Cannot connect to Redis")
    print("Connected to Redis")
    
    yield
    await app.state.redis.close()
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)
app.include_router(notes_router, prefix="/api/v1", tags=["notes"])


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True, port=5040)
