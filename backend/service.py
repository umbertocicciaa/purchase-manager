from fastapi import UploadFile
from repository import PurchaseRepository
from model import PurchaseCreate, PurchaseResponse
from typing import List, Optional
import uuid
import shutil
import os

class PurchaseService:
    """Service class for purchase business logic"""
    
    def __init__(self, repository: PurchaseRepository):
        self.repository = repository
        self.upload_folder = "./uploads"
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def upload_purchase(self, purchase_data: PurchaseCreate, receipt_file: UploadFile) -> dict:
        """Handle purchase upload with file storage"""
        file_path = None
        try:
            # Generate unique filename and save receipt
            file_id = str(uuid.uuid4())
            file_path = os.path.join(self.upload_folder, file_id + ".pdf")
            
            with open(file_path, "wb") as f:
                shutil.copyfileobj(receipt_file.file, f)
            
            # Create purchase in database
            purchase = self.repository.create_purchase(purchase_data, file_path)
            
            return {
                "message": "Purchase uploaded successfully.",
                "purchase_id": purchase.id,
                "receipt_path": file_path
            }
        except Exception as e:
            # Clean up file if database operation fails
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
            raise e
    
    def search_purchases(self, cf: Optional[str] = None) -> List[PurchaseResponse]:
        """Search purchases and return formatted results"""
        purchases = self.repository.search_purchases(cf)
        return [
            PurchaseResponse(
                id=p.id,
                customer_name=p.customer_name,
                customer_surname=p.customer_surname,
                customer_cf=p.customer_cf,
                credit_card=p.credit_card,
                product_name=p.product_name,
                price=p.price,
                date=p.date,
                receipt_path=p.receipt_path
            )
            for p in purchases
        ]
    
    def get_purchase_by_id(self, purchase_id: int) -> Optional[PurchaseResponse]:
        """Get a single purchase by ID"""
        purchase = self.repository.get_purchase_by_id(purchase_id)
        if purchase:
            return PurchaseResponse(
                id=purchase.id,
                customer_name=purchase.customer_name,
                customer_surname=purchase.customer_surname,
                customer_cf=purchase.customer_cf,
                credit_card=purchase.credit_card,
                product_name=purchase.product_name,
                price=purchase.price,
                date=purchase.date,
                receipt_path=purchase.receipt_path
            )
        return None
    
    def delete_purchase(self, purchase_id: int) -> bool:
        """Delete a purchase and its associated file"""
        purchase = self.repository.get_purchase_by_id(purchase_id)
        if purchase:
            # Remove file if it exists
            if purchase.receipt_path and os.path.exists(purchase.receipt_path):
                os.remove(purchase.receipt_path)
            
            # Delete from database
            return self.repository.delete_purchase(purchase_id)
        return False