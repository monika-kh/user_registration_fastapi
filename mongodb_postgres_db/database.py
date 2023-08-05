from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import models
import asyncpg
import motor.motor_asyncio
import local

app = FastAPI()

# PostgreSQL connection settings
POSTGRES_USER = local.POSTGRES_USER2
POSTGRES_PASSWORD = local.POSTGRES_PASSWORD2
POSTGRES_DB = local.POSTGRES_DB2
POSTGRES_HOST = local.POSTGRES_HOST2

# MongoDB connection settings
MONGO_HOST = local.MONGO_HOST
MONGO_PORT = local.MONGO_PORT
MONGO_DB = local.MONGO_DB

# PostgreSQL connection pool
async def get_postgres_pool():
    return await asyncpg.create_pool(
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
    )

# MongoDB client
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}")
mongo_db = mongo_client[MONGO_DB]