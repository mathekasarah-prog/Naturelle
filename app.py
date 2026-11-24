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

# DASHBOARD
if page == "Dashboard":

    products = get_products()

    total_products = len(products)

    inventory_value = sum(
        product[2] * product[3] for product in products
    )

    low_stock = sum(
        1 for product in products if product[3] <= 5
    )

    out_of_stock = sum(
        1 for product in products if product[3] == 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Products", total_products)

    col2.metric(
        "Inventory Value",
        f"KSh {inventory_value:,.2f}"
    )

    col3.metric("Low Stock", low_stock)

    col4.metric("Out of Stock", out_of_stock)
    
    st.subheader("Recent Inventory")

    st.dataframe(
        prepare_inventory_data(products),
        use_container_width=True,
        hide_index=True
    )
    
    
   # VIEW INVENTORY
elif page == "View Inventory":

    st.subheader("Inventory") 
    
    