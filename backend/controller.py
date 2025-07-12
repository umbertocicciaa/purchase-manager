from fastapi import Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from repository import PurchaseRepository
from service import PurchaseService
from model import PurchaseCreate, PurchaseResponse
from typing import List, Optional

class PurchaseController:
    """Controller class for handling purchase HTTP requests"""
    
    @staticmethod
    def get_service(db: Session = Depends(get_db)) -> PurchaseService:
        """Dependency to get purchase service"""
        repository = PurchaseRepository(db)
        return PurchaseService(repository)
    
    @staticmethod
    async def upload_purchase(
        customer_name: str = Form(...),
        customer_surname: str = Form(...),
        customer_cf: str = Form(...),
        credit_card: str = Form(...),
        product_name: str = Form(...),
        price: float = Form(...),
        date: str = Form(...),
        receipt: UploadFile = File(...),
        service: PurchaseService = Depends(get_service)
    ) -> dict:
        """Handle purchase upload endpoint"""
        try:
            purchase_data = PurchaseCreate(
                customer_name=customer_name,
                customer_surname=customer_surname,
                customer_cf=customer_cf,
                credit_card=credit_card,
                product_name=product_name,
                price=price,
                date=date
            )
            
            return service.upload_purchase(purchase_data, receipt)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload purchase: {str(e)}")
    
    @staticmethod
    def search_purchases(
        cf: Optional[str] = None,
        service: PurchaseService = Depends(get_service)
    ) -> List[PurchaseResponse]:
        """Handle purchase search endpoint"""
        try:
            return service.search_purchases(cf)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to search purchases: {str(e)}")
    
    @staticmethod
    def get_purchase(
        purchase_id: int,
        service: PurchaseService = Depends(get_service)
    ) -> PurchaseResponse:
        """Handle get single purchase endpoint"""
        try:
            purchase = service.get_purchase_by_id(purchase_id)
            if not purchase:
                raise HTTPException(status_code=404, detail="Purchase not found")
            return purchase
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get purchase: {str(e)}")
    
    @staticmethod
    def delete_purchase(
        purchase_id: int,
        service: PurchaseService = Depends(get_service)
    ) -> dict:
        """Handle delete purchase endpoint"""
        try:
            success = service.delete_purchase(purchase_id)
            if not success:
                raise HTTPException(status_code=404, detail="Purchase not found")
            return {"message": "Purchase deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete purchase: {str(e)}")
