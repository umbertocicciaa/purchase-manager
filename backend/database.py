from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base
import os

DATABASE_URL = "postgresql://postgres:postgres@postgres-db:5432/appdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
