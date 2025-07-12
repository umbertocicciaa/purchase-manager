"""
Service layer for API communication
"""
import requests
import streamlit as st
from typing import List, Optional, Dict, Any
from models import PurchaseData, SearchParams, PurchaseResponse
from config import config

class APIService:
    """Service class for handling API communications"""
    
    def __init__(self):
        self.base_url = config.BACKEND_URL
        self.endpoints = config.ENDPOINTS
    
    def upload_purchase(self, purchase_data: PurchaseData, receipt_file) -> Dict[str, Any]:
        """Upload a purchase with receipt file"""
        try:
            files = {"receipt": receipt_file.getvalue()}
            data = purchase_data.to_dict()
            
            response = requests.post(
                self.endpoints["upload"],
                data=data,
                files={"receipt": receipt_file}
            )
            
            if response.ok:
                return {
                    "success": True,
                    "message": response.json().get("message", "Upload successful"),
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "message": f"Upload failed: {response.text}",
                    "status_code": response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Connection error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Unexpected error: {str(e)}"
            }
    
    def search_purchases(self, search_params: SearchParams) -> Dict[str, Any]:
        """Search purchases based on parameters"""
        try:
            params = search_params.to_params()
            
            response = requests.get(
                self.endpoints["search"],
                params=params
            )
            
            if response.ok:
                purchases_data = response.json()
                purchases = [PurchaseResponse.from_dict(p) for p in purchases_data]
                return {
                    "success": True,
                    "data": purchases,
                    "count": len(purchases)
                }
            else:
                return {
                    "success": False,
                    "message": f"Search failed: {response.text}",
                    "status_code": response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Connection error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Unexpected error: {str(e)}"
            }
    
    def get_purchase_by_id(self, purchase_id: int) -> Dict[str, Any]:
        """Get a single purchase by ID"""
        try:
            response = requests.get(f"{self.endpoints['purchase']}/{purchase_id}")
            
            if response.ok:
                purchase_data = response.json()
                purchase = PurchaseResponse.from_dict(purchase_data)
                return {
                    "success": True,
                    "data": purchase
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to get purchase: {response.text}",
                    "status_code": response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Connection error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Unexpected error: {str(e)}"
            }
    
    def delete_purchase(self, purchase_id: int) -> Dict[str, Any]:
        """Delete a purchase by ID"""
        try:
            response = requests.delete(f"{self.endpoints['purchase']}/{purchase_id}")
            
            if response.ok:
                return {
                    "success": True,
                    "message": "Purchase deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to delete purchase: {response.text}",
                    "status_code": response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Connection error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Unexpected error: {str(e)}"
            }
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health status"""
        try:
            response = requests.get(self.endpoints["health"], timeout=5)
            
            if response.ok:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "message": "API is not responding properly"
                }
                
        except requests.exceptions.RequestException:
            return {
                "success": False,
                "message": "API is not reachable"
            }

# Global service instance
api_service = APIService()
