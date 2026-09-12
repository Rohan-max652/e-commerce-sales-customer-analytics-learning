import pandas as pd
from pathlib import Path

# ==========================================
# E-COMMERCE SALES & CUSTOMER ANALYTICS
# DATA CLEANING PIPELINE
# ==========================================

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"

# Create cleaned folder if it doesn't exist
CLEANED_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# 1. LOAD RAW DATA
# ==========================================

customers = pd.read_csv(RAW_DIR / "customers.csv")
products = pd.read_csv(RAW_DIR / "products.csv")
orders = pd.read_csv(RAW_DIR / "orders.csv")
order_items = pd.read_csv(RAW_DIR / "order_items.csv")

print("=" * 60)
print("RAW DATA LOADED")
print("=" * 60)

print(f"Customers:   {len(customers):,}")
print(f"Products:    {len(products):,}")
print(f"Orders:      {len(orders):,}")
print(f"Order Items: {len(order_items):,}")


# ==========================================
# 2. CLEAN CUSTOMERS
# ==========================================

print("\n" + "=" * 60)
print("CLEANING CUSTOMERS")
print("=" * 60)

customers_before = len(customers)

# Remove exact duplicate customer records
customers = customers.drop_duplicates()

duplicates_removed = customers_before - len(customers)

print(f"Duplicate rows removed: {duplicates_removed}")


# Fill missing ages with median age
median_age = customers["age"].median()

missing_age_before = customers["age"].isnull().sum()

customers["age"] = customers["age"].fillna(median_age)

print(f"Missing ages before cleaning: {missing_age_before}")
print(f"Median age used: {median_age}")
print(
    f"Missing ages after cleaning: "
    f"{customers['age'].isnull().sum()}"
)


# Standardize city names
customers["city"] = (
    customers["city"]
    .astype(str)
    .str.strip()
    .str.title()
)

print("City names standardized.")


# Convert age to integer
customers["age"] = customers["age"].astype(int)


# ==========================================
# 3. CLEAN PRODUCTS
# ==========================================

print("\n" + "=" * 60)
print("CLEANING PRODUCTS")
print("=" * 60)

# Convert prices to numeric
products["cost_price"] = pd.to_numeric(
    products["cost_price"],
    errors="coerce"
)

products["selling_price"] = pd.to_numeric(
    products["selling_price"],
    errors="coerce"
)

# Remove products with invalid prices
invalid_products = products[
    (products["cost_price"] <= 0) |
    (products["selling_price"] <= 0)
]

print(f"Invalid products found: {len(invalid_products)}")

products = products[
    (products["cost_price"] > 0) &
    (products["selling_price"] > 0)
].copy()

print(f"Products after cleaning: {len(products):,}")


# ==========================================
# 4. CLEAN ORDERS
# ==========================================

print("\n" + "=" * 60)
print("CLEANING ORDERS")
print("=" * 60)

# Convert order date to datetime
orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)

# Missing payment methods
missing_payment_before = orders["payment_method"].isnull().sum()

orders["payment_method"] = (
    orders["payment_method"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

print(
    f"Missing payment methods handled: "
    f"{missing_payment_before}"
)

print(
    f"Missing payment methods after cleaning: "
    f"{orders['payment_method'].isnull().sum()}"
)


# ==========================================
# 5. CLEAN ORDER ITEMS
# ==========================================

print("\n" + "=" * 60)
print("CLEANING ORDER ITEMS")
print("=" * 60)

order_items_before = len(order_items)

# Identify invalid quantities
invalid_quantity_count = (
    order_items["quantity"] <= 0
).sum()

print(
    f"Invalid quantity records found: "
    f"{invalid_quantity_count}"
)

# Keep only valid quantities
order_items = order_items[
    order_items["quantity"] > 0
].copy()

print(
    f"Order items removed: "
    f"{order_items_before - len(order_items)}"
)

print(
    f"Order items after cleaning: "
    f"{len(order_items):,}"
)


# ==========================================
# 6. FINAL DATA TYPE CLEANING
# ==========================================

order_items["quantity"] = order_items["quantity"].astype(int)

order_items["unit_price"] = pd.to_numeric(
    order_items["unit_price"],
    errors="coerce"
)


# ==========================================
# 7. SAVE CLEANED DATA
# ==========================================
customers = customers.rename(columns={"name": "customer_name"})

customers.to_csv(
    CLEANED_DIR / "customers_cleaned.csv",
    index=False
)

products.to_csv(
    CLEANED_DIR / "products_cleaned.csv",
    index=False
)

orders.to_csv(
    CLEANED_DIR / "orders_cleaned.csv",
    index=False
)

order_items.to_csv(
    CLEANED_DIR / "order_items_cleaned.csv",
    index=False
)


# ==========================================
# 8. CLEANING SUMMARY
# ==========================================

print("\n" + "=" * 60)
print("CLEANING COMPLETED")
print("=" * 60)

print(f"\nCustomers:")
print(f"Before: {customers_before:,}")
print(f"After:  {len(customers):,}")

print(f"\nProducts:")
print(f"After:  {len(products):,}")

print(f"\nOrders:")
print(f"After:  {len(orders):,}")

print(f"\nOrder Items:")
print(f"Before: {order_items_before:,}")
print(f"After:  {len(order_items):,}")

print("\nCleaned files saved to:")
print(CLEANED_DIR)

print("\nFiles created:")
print("1. customers_cleaned.csv")
print("2. products_cleaned.csv")
print("3. orders_cleaned.csv")
print("4. order_items_cleaned.csv")

print("\nData cleaning pipeline completed successfully!")