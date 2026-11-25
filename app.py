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
            "Quantity": product[3],
            "Category": product[4]
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
# Show a one-time message (set before a rerun)
if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))

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
    
    # Count products in each category
    category_counts = {}

    for product in products:
        category = product[4]

        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    col1, col2, col3, col4, col5 = st.columns(5)

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
    
    # Get all products
    all_products = get_products()

    # Get available categories
    categories = sorted({
        product[4] for product in all_products
    })

    # Add an option to view everything
    category_options = ["All categories"] + categories

    # Category dropdown
    selected_category = st.selectbox(
        "Filter by Category",
        category_options
    )

    # Search input
    search_term = st.text_input("Search by product name")

        # Search by name, or fall back to the category filter
    if search_term:
        filtered_products = search_products(search_term.strip())

        # Keep the category dropdown working with search
        if selected_category != "All categories":
            filtered_products = [
                product for product in filtered_products
                if product[4] == selected_category
            ]
    else:
        filtered_products = get_products(selected_category)

    # Display results
    if filtered_products:
        st.dataframe(
            prepare_inventory_data(filtered_products),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No products found.")
        
  #ADD PRODUCT      
elif page == "Add Product":

    st.subheader("Add New Product")

    category_options = [
        "Body Care",
        "Skin Care",
        "Hair Care",
        "Wellness",
        "Gift Sets"
    ]

    with st.form("add_product_form", clear_on_submit=True ):

        name = st.text_input("Product Name")

        price = st.number_input(
            "Price (KSh)",
            min_value=0.01,
            step=50.0
        )

        quantity = st.number_input(
            "Quantity",
            min_value=0,
            step=1
        )

        category = st.selectbox(
            "Product Category",
            category_options
        )

        submitted = st.form_submit_button("Add Product")

        if submitted:

            product = Product(name, price, quantity, category)

            if product.is_valid():

                try:
                    add_product(
                        name,
                        price,
                        quantity,
                        category
                    )

                    st.session_state["flash"] = f"{name} added successfully!"
                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error("A product with this name already exists.")

                except sqlite3.Error:
                    st.error("Something went wrong while adding the product.")

            else:
                st.error("Please enter valid product details.")
        
#UPDATE PRODUCTS
elif page == "Update Product":

    st.subheader("Update Product")

    products = get_products()

    if products:

        # Select the product to update
        product_ids = [product[0] for product in products]

        selected_id = st.selectbox(
            "Select Product ID",
            product_ids
        )

        # Find the selected product
        selected_product = next(
            product for product in products
            if product[0] == selected_id
        )

        # Available categories
        category_options = [
            "Body Care",
            "Skin Care",
            "Hair Care",
            "Wellness",
            "Gift Sets",
            "Uncategorized"
        ]

        # Update form
        with st.form("update_product_form"):

            name = st.text_input(
                "Product Name",
                value=selected_product[1]
            )

            price = st.number_input(
                "Price",
                min_value=0.01,
                value=float(selected_product[2])
            )

            quantity = st.number_input(
                "Quantity",
                min_value=0,
                value=int(selected_product[3])
            )

            category = st.selectbox(
                "Product Category",
                category_options,
                index=category_options.index(selected_product[4])
            )

            submitted = st.form_submit_button("Update Product")

            if submitted:

                product = Product(name, price, quantity, category)

                if product.is_valid():

                    try:
                        update_product(
                            selected_id,
                            name,
                            price,
                            quantity,
                            category
                        )

                        st.session_state["flash"] = "Product updated successfully!"
                        st.rerun()

                    except sqlite3.IntegrityError as e:
                        st.error(f"Database error: {e}")

                    except sqlite3.Error:
                        st.error("Something went wrong while updating the product.")

                else:
                    st.error("Please enter valid product details.")

    else:
        st.info("There are no products available to update.")
        
        
#DELETE PRODUCT
elif page == "Delete Product":

    st.subheader("Delete Product")

    products = get_products()

    if products:

        product_ids = [product[0] for product in products]

        selected_id = st.selectbox(
            "Select Product ID to Delete",
            product_ids
        )

        selected_product = next(
            product for product in products
            if product[0] == selected_id
        )

        st.warning(
            f"You are about to delete: {selected_product[1]}"
        )

        st.write(f"Category: {selected_product[4]}")
        st.write(f"Price: KSh {selected_product[2]:,.2f}")
        st.write(f"Quantity: {selected_product[3]}")

        confirm = st.checkbox(
            "I confirm that I want to delete this product."
        )

        if st.button("Delete Product", disabled=not confirm):

            try:
                deleted = delete_product(selected_id)

                if deleted:
                    st.success("Product deleted successfully!")
                    st.rerun()

                else:
                    st.warning("Product was not found.")

            except sqlite3.Error:
                st.error("Something went wrong while deleting the product.")

    else:
        st.info("There are no products available to delete.")


#EXPORT CSV
elif page == "Export CSV":

    st.subheader("Export Inventory to CSV")

    products = get_products()

    if products:

        try:
            output = io.StringIO()

            fieldnames = [
                "ID",
                "Name",
                "Price",
                "Quantity",
                "Category"
            ]

            writer = csv.DictWriter(
                output,
                fieldnames=fieldnames
            )

            writer.writeheader()

            writer.writerows(
                prepare_inventory_data(products)
            )

            csv_data = output.getvalue()

            st.download_button(
                label="Download Inventory CSV",
                data=csv_data,
                file_name="smartstock_inventory.csv",
                mime="text/csv"
            )

        except (csv.Error, OSError, ValueError):
            st.error("Unable to prepare the CSV file.")

    else:
        st.info("There are no products to export.")
        
        
        
        
        
