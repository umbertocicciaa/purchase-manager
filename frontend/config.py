"""
Configuration settings for the frontend application
"""
import os

class Config:
    """Application configuration"""
    
    # API Configuration
    BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
    
    # UI Configuration
    APP_TITLE = "Customer Purchase Manager"
    PAGE_TITLE = "Purchase Management System"
    PAGE_ICON = "🛍️"
    
    # Form Configuration
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES = ["pdf"]
    
    # API Endpoints
    ENDPOINTS = {
        "upload": f"{BACKEND_URL}/upload/",
        "search": f"{BACKEND_URL}/search",
        "purchase": f"{BACKEND_URL}/purchase",
        "health": f"{BACKEND_URL}/health"
    }

# Global config instance
config = Config()
