import pandas as pd

# =========================================================
# 1. LOAD CLEANED DATA
# =========================================================

customers = pd.read_csv("data/cleaned/customers_cleaned.csv")
products = pd.read_csv("data/cleaned/products_cleaned.csv")
orders = pd.read_csv("data/cleaned/orders_cleaned.csv")
order_items = pd.read_csv("data/cleaned/order_items_cleaned.csv")


# =========================================================
# 2. BASIC DATASET OVERVIEW
# =========================================================

print("\n========== DATASET OVERVIEW ==========")

print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)


# =========================================================
# 3. DATA TYPES
# =========================================================

print("\n========== DATA TYPES ==========")

print("\nCustomers:")
print(customers.dtypes)

print("\nProducts:")
print(products.dtypes)

print("\nOrders:")
print(orders.dtypes)

print("\nOrder Items:")
print(order_items.dtypes)


# =========================================================
# 4. MISSING VALUES
# =========================================================

print("\n========== MISSING VALUES ==========")

print("\nCustomers:")
print(customers.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

print("\nOrders:")
print(orders.isnull().sum())

print("\nOrder Items:")
print(order_items.isnull().sum())


# =========================================================
# 5. BASIC STATISTICS
# =========================================================

print("\n========== CUSTOMER STATISTICS ==========")

print(customers.describe())


print("\n========== PRODUCT STATISTICS ==========")

print(products.describe())


print("\n========== ORDER ITEM STATISTICS ==========")

print(order_items.describe())


# =========================================================
# 6. ORDER STATUS DISTRIBUTION
# =========================================================

print("\n========== ORDER STATUS ==========")

print(orders["status"].value_counts())


# =========================================================
# 7. PAYMENT METHOD DISTRIBUTION
# =========================================================

print("\n========== PAYMENT METHODS ==========")

print(orders["payment_method"].value_counts())


# =========================================================
# 8. PRODUCT CATEGORY DISTRIBUTION
# =========================================================

print("\n========== PRODUCT CATEGORIES ==========")

print(products["category"].value_counts())


# =========================================================
# 9. CUSTOMER CITY DISTRIBUTION
# =========================================================

print("\n========== TOP CUSTOMER CITIES ==========")

print(customers["city"].value_counts().head(10))


print("\n========== EDA COMPLETED ==========")