"""
Main application entry point for the Purchase Management System.
This file has been refactored to follow a clean architecture pattern.
"""
from pages import purchase_page

def main():
    """Main application function"""
    try:
        purchase_page.render()
    except Exception as e:
        import streamlit as st
        st.error(f"❌ Application Error: {str(e)}")
        st.info("🔄 Please refresh the page or contact support if the problem persists.")

if __name__ == "__main__":
    main()