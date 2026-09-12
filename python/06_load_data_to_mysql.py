import os
import pandas as pd
import mysql.connector
from pathlib import Path
from dotenv import load_dotenv


# ============================================================
# E-COMMERCE SALES & CUSTOMER ANALYTICS
# Load cleaned CSV data into MySQL
# ============================================================

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED_DIR = BASE_DIR / "data" / "cleaned"


# ------------------------------------------------------------
# 1. Read cleaned CSV files
# ------------------------------------------------------------

customers = pd.read_csv(CLEANED_DIR / "customers_cleaned.csv")
products = pd.read_csv(CLEANED_DIR / "products_cleaned.csv")
orders = pd.read_csv(CLEANED_DIR / "orders_cleaned.csv")
order_items = pd.read_csv(CLEANED_DIR / "order_items_cleaned.csv")


print("=" * 60)
print("LOADING CLEANED DATA INTO MYSQL")
print("=" * 60)

print(f"Customers:   {len(customers):,}")
print(f"Products:    {len(products):,}")
print(f"Orders:      {len(orders):,}")
print(f"Order Items: {len(order_items):,}")


# ------------------------------------------------------------
# 2. Connect to MySQL
# ------------------------------------------------------------

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

cursor = connection.cursor()

print("\nMySQL connection successful!")


# ------------------------------------------------------------
# 3. Insert Customers
# ------------------------------------------------------------

customer_query = """
INSERT INTO customers
(customer_id, customer_name, gender, age, city, state, signup_date)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

customer_data = [
    tuple(row)
    for row in customers[
        [
            "customer_id",
            "name",
            "gender",
            "age",
            "city",
            "state",
            "signup_date"
        ]
    ].itertuples(index=False, name=None)
]

cursor.executemany(customer_query, customer_data)

print(f"Customers inserted: {cursor.rowcount:,}")


# ------------------------------------------------------------
# 4. Insert Products
# ------------------------------------------------------------

product_query = """
INSERT INTO products
(product_id, product_name, category, brand, cost_price, selling_price)
VALUES (%s, %s, %s, %s, %s, %s)
"""

product_data = [
    tuple(row)
    for row in products[
        [
            "product_id",
            "product_name",
            "category",
            "brand",
            "cost_price",
            "selling_price"
        ]
    ].itertuples(index=False, name=None)
]

cursor.executemany(product_query, product_data)

print(f"Products inserted: {cursor.rowcount:,}")


# ------------------------------------------------------------
# 5. Insert Orders
# ------------------------------------------------------------

order_query = """
INSERT INTO orders
(order_id, customer_id, order_date, payment_method, discount, status)
VALUES (%s, %s, %s, %s, %s, %s)
"""

order_data = [
    tuple(row)
    for row in orders[
        [
            "order_id",
            "customer_id",
            "order_date",
            "payment_method",
            "discount",
            "status"
        ]
    ].itertuples(index=False, name=None)
]

cursor.executemany(order_query, order_data)

print(f"Orders inserted: {cursor.rowcount:,}")


# ------------------------------------------------------------
# 6. Insert Order Items
# ------------------------------------------------------------

order_item_query = """
INSERT INTO order_items
(order_item_id, order_id, product_id, quantity, unit_price)
VALUES (%s, %s, %s, %s, %s)
"""

order_item_data = [
    tuple(row)
    for row in order_items[
        [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price"
        ]
    ].itertuples(index=False, name=None)
]

cursor.executemany(order_item_query, order_item_data)

print(f"Order items inserted: {cursor.rowcount:,}")


# ------------------------------------------------------------
# 7. Commit all changes
# ------------------------------------------------------------

connection.commit()

print("\n" + "=" * 60)
print("DATA LOADING COMPLETED SUCCESSFULLY!")
print("=" * 60)


# ------------------------------------------------------------
# 8. Close connection
# ------------------------------------------------------------

cursor.close()
connection.close()

print("MySQL connection closed.")