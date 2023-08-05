from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg
import motor.motor_asyncio

app = FastAPI()

# PostgreSQL connection settings
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD= "root"
POSTGRES_DB = "fastapi_db"
POSTGRES_HOST = "localhost"

# MongoDB connection settings
MONGO_HOST = "localhost"
MONGO_PORT = "5432"
MONGO_DB = "fastapi_mmongodb"

# PostgreSQL connection pool
async def get_postgres_pool():
    return await asyncpg.create_pool(
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
    )

# MongoDB client
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}")
mongo_db = mongo_client[MONGO_DB]