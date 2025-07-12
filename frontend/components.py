"""
Reusable UI components for the application
"""
import streamlit as st
from datetime import date
from typing import Optional, Tuple, List
from models import PurchaseData, SearchParams, PurchaseResponse
from utils import validator, formatter, file_utils

class UIComponents:
    """Collection of reusable UI components"""
    
    @staticmethod
    def render_header():
        """Render application header"""
        st.set_page_config(
            page_title="Purchase Management System",
            page_icon="🛍️",
            layout="wide"
        )
        st.title("🛍️ Customer Purchase Manager")
        st.markdown("---")
    
    @staticmethod
    def render_upload_form() -> Tuple[Optional[PurchaseData], Optional[object]]:
        """Render purchase upload form"""
        st.subheader("📤 Insert New Purchase")
        
        with st.form("purchase_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Customer Name*", help="Enter customer's first name")
                surname = st.text_input("Customer Surname*", help="Enter customer's last name")
                cf = st.text_input("Codice Fiscale*", help="Enter customer's tax code")
                cc = st.text_input("Credit Card*", help="Enter credit card number")
            
            with col2:
                product = st.text_input("Product Name*", help="Enter product name")
                price = st.number_input("Price (€)*", min_value=0.01, step=0.01, help="Enter product price")
                purchase_date = st.date_input("Purchase Date*", value=date.today(), help="Select purchase date")
                receipt = st.file_uploader("Receipt (PDF)*", type=["pdf"], help="Upload purchase receipt")
            
            submitted = st.form_submit_button("📤 Submit Purchase", use_container_width=True)
            
            if submitted:
                # Validation
                validation_errors = []
                
                # Validate required fields
                if not all([name, surname, cf, cc, product, receipt]):
                    validation_errors.append("Please fill in all required fields marked with *")
                
                # Validate individual fields
                if name:
                    name_validation = validator.validate_name(name, "Customer Name")
                    if not name_validation["valid"]:
                        validation_errors.append(name_validation["message"])
                
                if surname:
                    surname_validation = validator.validate_name(surname, "Customer Surname")
                    if not surname_validation["valid"]:
                        validation_errors.append(surname_validation["message"])
                
                if cf:
                    cf_validation = validator.validate_codice_fiscale(cf)
                    if not cf_validation["valid"]:
                        validation_errors.append(cf_validation["message"])
                
                if cc:
                    cc_validation = validator.validate_credit_card(cc)
                    if not cc_validation["valid"]:
                        validation_errors.append(cc_validation["message"])
                
                if price:
                    price_validation = validator.validate_price(price)
                    if not price_validation["valid"]:
                        validation_errors.append(price_validation["message"])
                
                if receipt:
                    file_size_validation = file_utils.validate_file_size(receipt.size)
                    if not file_size_validation["valid"]:
                        validation_errors.append(file_size_validation["message"])
                
                # Show validation errors
                if validation_errors:
                    for error in validation_errors:
                        st.error(f"⚠️ {error}")
                    return None, None
                
                purchase_data = PurchaseData.from_form_data(
                    name, surname, cf, cc, product, price, purchase_date
                )
                return purchase_data, receipt
            
            return None, None
    
    @staticmethod
    def render_search_form() -> Optional[SearchParams]:
        """Render search form"""
        st.subheader("🔍 Search Purchases")
        
        with st.expander("Search Filters", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                search_name = st.text_input("Name", help="Search by customer name")
                search_surname = st.text_input("Surname", help="Search by customer surname")
            
            with col2:
                search_cf = st.text_input("Codice Fiscale", help="Search by tax code")
                search_cc = st.text_input("Credit Card", help="Search by credit card")
            
            with col3:
                search_product = st.text_input("Product", help="Search by product name")
                search_date = st.date_input("Date", value=None, help="Search by purchase date")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("🔍 Search", use_container_width=True):
                    return SearchParams(
                        name=search_name or None,
                        surname=search_surname or None,
                        cf=search_cf or None,
                        cc=search_cc or None,
                        product=search_product or None,
                        date=str(search_date) if search_date else None
                    )
            
            with col2:
                if st.button("🔄 Clear", use_container_width=True):
                    st.rerun()
        
        return None
    
    @staticmethod
    def render_purchase_results(purchases: List[PurchaseResponse], show_actions: bool = True):
        """Render purchase search results"""
        if not purchases:
            st.info("📭 No purchases found matching your criteria.")
            return
        
        st.success(f"📊 Found {len(purchases)} purchase(s)")
        
        for i, purchase in enumerate(purchases):
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    **🆔 Purchase #{purchase.id}**
                    - **👤 Customer:** {purchase.customer_name} {purchase.customer_surname}
                    - **🆔 CF:** {purchase.customer_cf}
                    - **💳 Card:** {formatter.format_credit_card(purchase.credit_card)}
                    - **🛍️ Product:** {formatter.truncate_text(purchase.product_name, 40)}
                    - **💰 Price:** {formatter.format_currency(purchase.price)}
                    - **📅 Date:** {formatter.format_date(purchase.date)}
                    - **📄 Receipt:** {purchase.receipt_path.split('/')[-1] if purchase.receipt_path else 'N/A'}
                    """)
                
                if show_actions:
                    with col2:
                        if st.button(f"🗑️ Delete", key=f"delete_{purchase.id}"):
                            st.session_state[f"confirm_delete_{purchase.id}"] = True
                
                st.markdown("---")
    
    @staticmethod
    def render_success_message(message: str):
        """Render success message"""
        st.success(f"✅ {message}")
    
    @staticmethod
    def render_error_message(message: str):
        """Render error message"""
        st.error(f"❌ {message}")
    
    @staticmethod
    def render_warning_message(message: str):
        """Render warning message"""
        st.warning(f"⚠️ {message}")
    
    @staticmethod
    def render_info_message(message: str):
        """Render info message"""
        st.info(f"ℹ️ {message}")
    
    @staticmethod
    def render_loading():
        """Render loading spinner"""
        return st.spinner("⏳ Processing...")
    
    @staticmethod
    def render_sidebar_info():
        """Render sidebar with application info"""
        with st.sidebar:
            st.markdown("## 📋 Application Info")
            st.markdown("""
            **Purchase Management System**
            
            This application allows you to:
            - 📤 Upload new purchases with receipts
            - 🔍 Search existing purchases
            - 📊 View purchase details
            - 🗑️ Delete purchases
            
            **Need Help?**
            - Fill all required fields marked with *
            - Upload receipts in PDF format only
            - Use search filters to find specific purchases
            """)
            
            st.markdown("---")
            st.markdown("**Quick Stats**")
            # These could be populated with real data
            st.metric("Today's Uploads", "0")
            st.metric("Total Purchases", "0")

# Global components instance
ui = UIComponents()
