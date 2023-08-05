from typing import Annotated
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class UserRegistration(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str
    profile_picture: str = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/register/")
async def register_user(user_data: UserRegistration, db: db_dependency):
    db = SessionLocal()
    try:
        existing_user_email = (
            db.query(models.User).filter(models.User.email == user_data.email).first()
        )
        if existing_user_email:
            raise HTTPException(status_code=400, detail="Email already exists.")

        existing_user_phone = (
            db.query(models.User).filter(models.User.phone == user_data.phone).first()
        )
        if existing_user_phone:
            raise HTTPException(status_code=400, detail="Phone number already exists.")

        new_user = models.User(
            full_name=user_data.full_name,
            email=user_data.email,
            password=user_data.password,
            phone=user_data.phone,
        )
        db.add(new_user)
        db.commit()

        if user_data.profile_picture:
            new_profile = models.Profile(
                profile_picture=user_data.profile_picture, user=new_user
            )
            db.add(new_profile)
            db.commit()

        return {"message": "User registered successfully."}

    finally:
        db.close()


@app.get("/users/{user_id}")
async def get_user_details(user_id: int):
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user
