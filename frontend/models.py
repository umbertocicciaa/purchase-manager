"""
Data models for the frontend application
"""
from datetime import date
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class PurchaseData:
    """Data model for purchase information"""
    customer_name: str
    customer_surname: str
    customer_cf: str
    credit_card: str
    product_name: str
    price: float
    date: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests"""
        return {
            "customer_name": self.customer_name,
            "customer_surname": self.customer_surname,
            "customer_cf": self.customer_cf,
            "credit_card": self.credit_card,
            "product_name": self.product_name,
            "price": self.price,
            "date": self.date
        }
    
    @classmethod
    def from_form_data(cls, name: str, surname: str, cf: str, cc: str, 
                      product: str, price: float, purchase_date: date):
        """Create PurchaseData from form inputs"""
        return cls(
            customer_name=name,
            customer_surname=surname,
            customer_cf=cf,
            credit_card=cc,
            product_name=product,
            price=price,
            date=str(purchase_date)
        )

@dataclass
class SearchParams:
    """Data model for search parameters"""
    name: Optional[str] = None
    surname: Optional[str] = None
    cf: Optional[str] = None
    cc: Optional[str] = None
    product: Optional[str] = None
    date: Optional[str] = None
    
    def to_params(self) -> Dict[str, str]:
        """Convert to query parameters, excluding None values"""
        params = {}
        if self.name:
            params["name"] = self.name
        if self.surname:
            params["surname"] = self.surname
        if self.cf:
            params["cf"] = self.cf
        if self.cc:
            params["cc"] = self.cc
        if self.product:
            params["product"] = self.product
        if self.date:
            params["date"] = self.date
        return params

@dataclass
class PurchaseResponse:
    """Data model for purchase API response"""
    id: int
    customer_name: str
    customer_surname: str
    customer_cf: str
    credit_card: str
    product_name: str
    price: float
    date: str
    receipt_path: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PurchaseResponse':
        """Create PurchaseResponse from API response"""
        return cls(
            id=data["id"],
            customer_name=data["customer_name"],
            customer_surname=data["customer_surname"],
            customer_cf=data["customer_cf"],
            credit_card=data["credit_card"],
            product_name=data["product_name"],
            price=data["price"],
            date=data["date"],
            receipt_path=data["receipt_path"]
        )
