from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String, unique=True, index=True)

    profile = relationship("Profile", uselist=False, back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    profile_picture = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="profile")
