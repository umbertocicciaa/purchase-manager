from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class PurchaseDB(Base):
    """SQLAlchemy model for purchase database table"""
    __tablename__ = "purchases"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    customer_surname = Column(String)
    customer_cf = Column(String, index=True)
    credit_card = Column(String)
    product_name = Column(String)
    price = Column(Float)
    date = Column(String)
    receipt_path = Column(String)

class PurchaseCreate(BaseModel):
    """Pydantic model for creating a purchase"""
    customer_name: str
    customer_surname: str
    customer_cf: str
    credit_card: str
    product_name: str
    price: float
    date: str

class PurchaseResponse(BaseModel):
    """Pydantic model for purchase response"""
    id: int
    customer_name: str
    customer_surname: str
    customer_cf: str
    credit_card: str
    product_name: str
    price: float
    date: str
    receipt_path: str

    class Config:
        from_attributes = True

class PurchaseSearchParams(BaseModel):
    """Pydantic model for search parameters"""
    cf: Optional[str] = None