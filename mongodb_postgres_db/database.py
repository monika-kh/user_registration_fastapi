from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg
import motor.motor_asyncio

import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

# PostgreSQL connection settings
POSTGRES_USER =  os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")

# MongoDB connection settings
MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")
MONGO_DB = os.environ.get("MONGO_DB")

# PostgreSQL connection pool
async def get_postgres_pool():
    return await asyncpg.create_pool(
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
    )

# MongoDB client
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}")
mongo_db = mongo_client[MONGO_DB]