import streamlit as st
import sqlite3
import csv
import io

def prepare_inventory_data(products):
    return [
        {
            "ID": product[0],
            "Name": product[1],
            "Price": product[2],
            "Quantity": product[3]
        }
        for product in products
    ]
from database import (
    initialize_db,
    load_sample_products,
    add_product,
    get_products,
    search_products,
    update_product,
    delete_product
)

from products import Product


# PAGE CONFIGURATION
st.set_page_config(
    page_title="SmartStock",
    page_icon="🧠",
    layout="wide"
)

# INITIALIZE DATABASE
initialize_db()
load_sample_products()


# APPLICATION TITLE
st.title("🧠 SmartStock")
st.caption("Small Business Inventory Management System")

# NAVIGATION
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "View Inventory",
        "Add Product",
        "Update Product",
        "Delete Product",
        "Export CSV"
    ]
)
