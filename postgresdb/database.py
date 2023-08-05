from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import local

SQLALCHEMY_DATABASE_URL = f"postgresql://{local.POSTGRES_USER}:{local.POSTGRES_PASSWORD}@{local.POSTGRES_HOST}/{local.POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
