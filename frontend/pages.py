"""
Page logic and state management
"""
import streamlit as st
from services import api_service
from components import ui
from models import SearchParams

class PurchaseManagerPage:
    """Main page controller for purchase management"""
    
    def __init__(self):
        self.api_service = api_service
        self.ui = ui
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state variables"""
        if 'search_results' not in st.session_state:
            st.session_state.search_results = []
        if 'last_search_params' not in st.session_state:
            st.session_state.last_search_params = None
    
    def render(self):
        """Render the main page"""
        # Header
        self.ui.render_header()
        
        # Sidebar
        self.ui.render_sidebar_info()
        
        # Main content
        self._render_main_content()
    
    def _render_main_content(self):
        """Render main content area"""
        # Upload section
        self._render_upload_section()
        
        st.markdown("---")
        
        # Search section
        self._render_search_section()
    
    def _render_upload_section(self):
        """Render upload purchase section"""
        purchase_data, receipt_file = self.ui.render_upload_form()
        
        if purchase_data and receipt_file:
            with self.ui.render_loading():
                result = self.api_service.upload_purchase(purchase_data, receipt_file)
            
            if result["success"]:
                self.ui.render_success_message(result["message"])
                # Clear form by rerunning
                st.balloons()
            else:
                self.ui.render_error_message(result["message"])
    
    def _render_search_section(self):
        """Render search purchases section"""
        search_params = self.ui.render_search_form()
        
        # Handle search
        if search_params:
            with self.ui.render_loading():
                result = self.api_service.search_purchases(search_params)
            
            if result["success"]:
                st.session_state.search_results = result["data"]
                st.session_state.last_search_params = search_params
                if result["count"] > 0:
                    self.ui.render_info_message(f"Found {result['count']} purchase(s)")
            else:
                self.ui.render_error_message(result["message"])
                st.session_state.search_results = []
        
        # Display results
        if st.session_state.search_results:
            self._render_results_section()
    
    def _render_results_section(self):
        """Render search results section"""
        st.subheader("📊 Search Results")
        
        purchases = st.session_state.search_results
        
        # Handle delete actions
        purchases_to_keep = []
        for purchase in purchases:
            delete_key = f"confirm_delete_{purchase.id}"
            
            if delete_key in st.session_state and st.session_state[delete_key]:
                # Show confirmation dialog
                with st.container():
                    st.warning(f"⚠️ Are you sure you want to delete purchase #{purchase.id}?")
                    col1, col2, col3 = st.columns([1, 1, 2])
                    
                    with col1:
                        if st.button("✅ Yes, Delete", key=f"confirm_yes_{purchase.id}"):
                            with self.ui.render_loading():
                                delete_result = self.api_service.delete_purchase(purchase.id)
                            
                            if delete_result["success"]:
                                self.ui.render_success_message("Purchase deleted successfully")
                                # Remove from session state
                                del st.session_state[delete_key]
                                # Refresh search results
                                if st.session_state.last_search_params:
                                    result = self.api_service.search_purchases(st.session_state.last_search_params)
                                    if result["success"]:
                                        st.session_state.search_results = result["data"]
                                st.rerun()
                            else:
                                self.ui.render_error_message(delete_result["message"])
                                del st.session_state[delete_key]
                    
                    with col2:
                        if st.button("❌ Cancel", key=f"confirm_no_{purchase.id}"):
                            del st.session_state[delete_key]
                            st.rerun()
                    
                    st.markdown("---")
            else:
                purchases_to_keep.append(purchase)
        
        # Render purchases that are not being deleted
        self.ui.render_purchase_results(purchases_to_keep, show_actions=True)
        
        # Add export option
        if purchases_to_keep:
            self._render_export_section(purchases_to_keep)
    
    def _render_export_section(self, purchases):
        """Render export options"""
        st.subheader("📥 Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export as CSV"):
                csv_data = self._generate_csv(purchases)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name="purchases_export.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📋 Copy Summary"):
                summary = self._generate_summary(purchases)
                st.code(summary, language="text")
    
    def _generate_csv(self, purchases):
        """Generate CSV data from purchases"""
        import io
        import csv
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            "ID", "Customer Name", "Customer Surname", "Codice Fiscale",
            "Credit Card", "Product", "Price", "Date", "Receipt Path"
        ])
        
        # Data
        for purchase in purchases:
            writer.writerow([
                purchase.id, purchase.customer_name, purchase.customer_surname,
                purchase.customer_cf, purchase.credit_card, purchase.product_name,
                purchase.price, purchase.date, purchase.receipt_path
            ])
        
        return output.getvalue()
    
    def _generate_summary(self, purchases):
        """Generate text summary of purchases"""
        total_amount = sum(p.price for p in purchases)
        unique_customers = len(set(p.customer_cf for p in purchases))
        
        summary = f"""Purchase Summary
================
Total Purchases: {len(purchases)}
Unique Customers: {unique_customers}
Total Amount: €{total_amount:.2f}
Average Purchase: €{total_amount/len(purchases):.2f}

Recent Purchases:
"""
        
        for purchase in purchases[:5]:  # Show only first 5
            summary += f"- {purchase.customer_name} {purchase.customer_surname}: €{purchase.price:.2f} ({purchase.product_name})\n"
        
        if len(purchases) > 5:
            summary += f"... and {len(purchases) - 5} more purchases"
        
        return summary

# Global page instance
purchase_page = PurchaseManagerPage()
