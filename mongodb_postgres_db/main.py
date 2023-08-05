from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import models
import database
import asyncpg
import motor.motor_asyncio

app = FastAPI()


# Registration Route
@app.post("/register/")
async def register_user(user: BaseModel.UserRegistration):
    postgres_pool = await database.get_postgres_pool()

    # Check if email already exists in PostgreSQL
    email_exists = await postgres_pool.fetchval(
        "SELECT EXISTS (SELECT 1 FROM users WHERE email = $1)", user.email
    )
    if email_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Insert user details in PostgreSQL
    async with postgres_pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO users (first_name, password, email, phone) VALUES ($1, $2, $3, $4)",
            user.first_name,
            user.password,
            user.email,
            user.phone,
        )

    # Insert profile picture in MongoDB
    await database.mongo_db.users.insert_one({"email": user.email, "profile_picture": user.profile_picture})

    return {"message": "User registered successfully"}

# Get User Details Route
@app.get("/users/{user_id}")
async def get_user_details(user_id: int):
    postgres_pool = await database.get_postgres_pool()

    # Fetch user details from PostgreSQL
    user_data = await postgres_pool.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch profile picture from MongoDB
    user_profile = await database.mongo_db.users.find_one({"email": user_data["email"]})
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    user_data["profile_picture"] = user_profile["profile_picture"]
    return user_data
