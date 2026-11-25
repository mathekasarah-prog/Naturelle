
# SmartStock — Inventory Management System

SmartStock is a small-business inventory management application
built with Python, Streamlit, and SQLite.

It helps small businesses manage their product inventory by
allowing them to add, view, search, filter, update, delete,
and export product records.

The application also provides a dashboard for monitoring
inventory levels, product quantities, and the estimated
value of inventory held in stock.

## Features

- Dashboard displaying inventory statistics
- Total number of products
- Total inventory value
- Low-stock monitoring
- Out-of-stock monitoring
- Product inventory listing
- Product search by name
- Inventory filtering by category
- Add new products
- Update existing products
- Delete products with confirmation
- Product validation
- SQLite database storage
- Export inventory to CSV

## Technologies Used

- Python
- Streamlit
- SQLite
- CSV
- Git

## Project Structure

SmartStock/
│
├── app.py
├── database.py
├── products.py
├── inventory.db
├── requirements.txt
├── README.md
└── .gitignore

## Installation

### 1. Clone the repository

git clone <your-repository-url>

### 2. Navigate into the project directory

cd SmartStock

### 3. Create a virtual environment

python -m venv .venv

### 4. Activate the virtual environment

Windows:

.venv\Scripts\activate

### 5. Install dependencies

pip install -r requirements.txt

### 6. Run the application

streamlit run app.py

The application will open in your browser.

## Application Architecture

SmartStock separates its responsibilities into three
main Python modules.

### app.py

Handles the user interface and application logic.

It includes the dashboard, product listing, search,
category filtering, product forms, deletion controls,
and CSV downloading.

### database.py

Handles database operations, including:

- Initializing the database
- Loading sample products
- Adding products
- Retrieving products
- Searching products
- Updating products
- Deleting products

### products.py

Contains the Product class, product validation logic,
inventory value calculations, and sample product data.

## Database

SmartStock uses SQLite to store inventory records.

The products table stores:

- ID
- Name
- Price
- Quantity
- Category

SQLite allows the application to persist inventory data
without requiring a separate database server.

## Inventory Value

The inventory value of an individual product is calculated as:

Price × Quantity

The total inventory value is calculated by summing the
inventory value of all products.

## Validation

Products are validated before being added or updated.

Validation checks include:

- Product names must be valid and non-empty.
- Prices must be positive numeric values.
- Quantities must be non-negative integers.
- Categories must be valid and non-empty.

The database also enforces constraints such as unique
product names and non-null fields.

## CSV Export

Users can export inventory records into a CSV file
that can be opened using spreadsheet applications
such as Microsoft Excel.

## Future Improvements

- User authentication and role-based access
- Stock movement tracking
- Sales and purchase records
- Automatic low-stock alerts
- Inventory analytics and charts
- Product barcode support
- Supplier management
- Database backup and restore
- Improved reporting
- Automated testing

## Author

Developed as a Python learning and portfolio project.
