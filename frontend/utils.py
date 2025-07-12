"""
Utility functions for the frontend application
"""
import re
from typing import Dict, Any, Optional
from datetime import date, datetime

class ValidationUtils:
    """Utility class for data validation"""
    
    @staticmethod
    def validate_codice_fiscale(cf: str) -> Dict[str, Any]:
        """Validate Italian Codice Fiscale format"""
        if not cf:
            return {"valid": False, "message": "Codice Fiscale is required"}
        
        # Basic format check (16 characters, alphanumeric)
        if len(cf) != 16:
            return {"valid": False, "message": "Codice Fiscale must be 16 characters long"}
        
        if not re.match(r'^[A-Z0-9]{16}$', cf.upper()):
            return {"valid": False, "message": "Codice Fiscale must contain only letters and numbers"}
        
        return {"valid": True, "message": "Valid Codice Fiscale"}
    
    @staticmethod
    def validate_credit_card(cc: str) -> Dict[str, Any]:
        """Basic credit card validation"""
        if not cc:
            return {"valid": False, "message": "Credit card number is required"}
        
        # Remove spaces and hyphens
        cc_clean = re.sub(r'[\s-]', '', cc)
        
        # Check if all digits
        if not cc_clean.isdigit():
            return {"valid": False, "message": "Credit card must contain only numbers"}
        
        # Check length (13-19 digits for most cards)
        if not (13 <= len(cc_clean) <= 19):
            return {"valid": False, "message": "Credit card must be between 13-19 digits"}
        
        return {"valid": True, "message": "Valid credit card format"}
    
    @staticmethod
    def validate_price(price: float) -> Dict[str, Any]:
        """Validate price value"""
        if price <= 0:
            return {"valid": False, "message": "Price must be greater than 0"}
        
        if price > 999999.99:
            return {"valid": False, "message": "Price is too high (max: €999,999.99)"}
        
        return {"valid": True, "message": "Valid price"}
    
    @staticmethod
    def validate_name(name: str, field_name: str) -> Dict[str, Any]:
        """Validate name fields"""
        if not name or not name.strip():
            return {"valid": False, "message": f"{field_name} is required"}
        
        if len(name.strip()) < 2:
            return {"valid": False, "message": f"{field_name} must be at least 2 characters long"}
        
        if len(name.strip()) > 50:
            return {"valid": False, "message": f"{field_name} must be less than 50 characters"}
        
        # Allow only letters, spaces, apostrophes, and hyphens
        if not re.match(r"^[A-Za-zÀ-ÿ\s'-]+$", name.strip()):
            return {"valid": False, "message": f"{field_name} contains invalid characters"}
        
        return {"valid": True, "message": f"Valid {field_name.lower()}"}

class FormatUtils:
    """Utility class for data formatting"""
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """Format amount as currency"""
        return f"€{amount:,.2f}"
    
    @staticmethod
    def format_date(date_str: str) -> str:
        """Format date string for display"""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%d/%m/%Y")
        except:
            return date_str
    
    @staticmethod
    def format_credit_card(cc: str) -> str:
        """Format credit card for display (masked)"""
        if len(cc) < 4:
            return "*" * len(cc)
        return "*" * (len(cc) - 4) + cc[-4:]
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 30) -> str:
        """Truncate text with ellipsis"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."

class FileUtils:
    """Utility class for file operations"""
    
    @staticmethod
    def validate_file_size(file_size: int, max_size: int = 10 * 1024 * 1024) -> Dict[str, Any]:
        """Validate file size (default max: 10MB)"""
        if file_size > max_size:
            max_mb = max_size / (1024 * 1024)
            current_mb = file_size / (1024 * 1024)
            return {
                "valid": False, 
                "message": f"File too large ({current_mb:.1f}MB). Maximum size: {max_mb:.1f}MB"
            }
        return {"valid": True, "message": "Valid file size"}
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size for display"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"

class SessionUtils:
    """Utility class for session management"""
    
    @staticmethod
    def clear_session_state(keys_to_keep: Optional[list] = None):
        """Clear session state except for specified keys"""
        import streamlit as st
        
        if keys_to_keep is None:
            keys_to_keep = []
        
        keys_to_remove = [key for key in st.session_state.keys() if key not in keys_to_keep]
        for key in keys_to_remove:
            del st.session_state[key]
    
    @staticmethod
    def get_session_value(key: str, default=None):
        """Safely get session state value"""
        import streamlit as st
        return st.session_state.get(key, default)
    
    @staticmethod
    def set_session_value(key: str, value):
        """Set session state value"""
        import streamlit as st
        st.session_state[key] = value

# Global utility instances
validator = ValidationUtils()
formatter = FormatUtils()
file_utils = FileUtils()
session_utils = SessionUtils()
