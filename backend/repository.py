from sqlalchemy.orm import Session
from model import PurchaseDB, PurchaseCreate
from typing import List, Optional

class PurchaseRepository:
    """Repository class for handling purchase data operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_purchase(self, purchase_data: PurchaseCreate, receipt_path: str) -> PurchaseDB:
        """Create a new purchase in the database"""
        db_purchase = PurchaseDB(
            customer_name=purchase_data.customer_name,
            customer_surname=purchase_data.customer_surname,
            customer_cf=purchase_data.customer_cf,
            credit_card=purchase_data.credit_card,
            product_name=purchase_data.product_name,
            price=purchase_data.price,
            date=purchase_data.date,
            receipt_path=receipt_path
        )
        self.db.add(db_purchase)
        self.db.commit()
        self.db.refresh(db_purchase)
        return db_purchase
    
    def get_purchase_by_id(self, purchase_id: int) -> Optional[PurchaseDB]:
        """Get a purchase by its ID"""
        return self.db.query(PurchaseDB).filter(PurchaseDB.id == purchase_id).first()
    
    def search_purchases(self, cf: Optional[str] = None) -> List[PurchaseDB]:
        """Search purchases with optional customer CF filter"""
        query = self.db.query(PurchaseDB)
        if cf:
            query = query.filter(PurchaseDB.customer_cf.ilike(f"%{cf}%"))
        return query.all()
    
    def get_all_purchases(self) -> List[PurchaseDB]:
        """Get all purchases"""
        return self.db.query(PurchaseDB).all()
    
    def delete_purchase(self, purchase_id: int) -> bool:
        """Delete a purchase by its ID"""
        purchase = self.get_purchase_by_id(purchase_id)
        if purchase:
            self.db.delete(purchase)
            self.db.commit()
            return True
        return False