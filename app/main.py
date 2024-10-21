from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import router as api_router
from app.api.services.redis.redis_service import pool, redis_url, redis_port, redis_db
import redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Redis pool
    global pool
    pool = redis.ConnectionPool(host=redis_url, port=redis_port, db=redis_db)
    yield
    # Close Redis pool
    pool.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
