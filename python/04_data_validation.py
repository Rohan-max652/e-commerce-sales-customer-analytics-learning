import pandas as pd
from pathlib import Path

# ==========================================
# E-COMMERCE SALES & CUSTOMER ANALYTICS
# CLEANED DATA VALIDATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED_DIR = BASE_DIR / "data" / "cleaned"

customers = pd.read_csv(CLEANED_DIR / "customers_cleaned.csv")
products = pd.read_csv(CLEANED_DIR / "products_cleaned.csv")
orders = pd.read_csv(CLEANED_DIR / "orders_cleaned.csv")
order_items = pd.read_csv(CLEANED_DIR / "order_items_cleaned.csv")

print("=" * 70)
print("CLEANED DATA VALIDATION")
print("=" * 70)

# --------------------------------------------------
# 1. BASIC RECORD COUNTS
# --------------------------------------------------

print("\n" + "=" * 70)
print("1. BASIC RECORD COUNTS")
print("=" * 70)

print(f"Customers:   {len(customers):,}")
print(f"Products:    {len(products):,}")
print(f"Orders:      {len(orders):,}")
print(f"Order Items: {len(order_items):,}")

# --------------------------------------------------
# 2. MISSING VALUES
# --------------------------------------------------

print("\n" + "=" * 70)
print("2. MISSING VALUE CHECK")
print("=" * 70)

print("\nCustomers:")
print(customers.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

print("\nOrders:")
print(orders.isnull().sum())

print("\nOrder Items:")
print(order_items.isnull().sum())

# --------------------------------------------------
# 3. DUPLICATE CHECK
# --------------------------------------------------

print("\n" + "=" * 70)
print("3. DUPLICATE CHECK")
print("=" * 70)

print(f"Duplicate customer rows: {customers.duplicated().sum()}")
print(f"Duplicate customer IDs: {customers['customer_id'].duplicated().sum()}")

print(f"Duplicate product rows: {products.duplicated().sum()}")
print(f"Duplicate product IDs: {products['product_id'].duplicated().sum()}")

print(f"Duplicate order rows: {orders.duplicated().sum()}")
print(f"Duplicate order IDs: {orders['order_id'].duplicated().sum()}")

print(f"Duplicate order-item rows: {order_items.duplicated().sum()}")
print(f"Duplicate order-item IDs: {order_items['order_item_id'].duplicated().sum()}")

# --------------------------------------------------
# 4. CUSTOMER DATA VALIDATION
# --------------------------------------------------

print("\n" + "=" * 70)
print("4. CUSTOMER DATA VALIDATION")
print("=" * 70)

invalid_age = ((customers["age"] < 18) | (customers["age"] > 60)).sum()

print(f"Invalid ages: {invalid_age}")

# Check city formatting
city_format_issues = (
    customers["city"].astype(str)
    .str.strip()
    .str.title()
    .ne(customers["city"].astype(str))
).sum()

print(f"City formatting issues: {city_format_issues}")

# --------------------------------------------------
# 5. PRODUCT DATA VALIDATION
# --------------------------------------------------

print("\n" + "=" * 70)
print("5. PRODUCT DATA VALIDATION")
print("=" * 70)

invalid_cost_price = (products["cost_price"] <= 0).sum()
invalid_selling_price = (products["selling_price"] <= 0).sum()
cost_greater_than_selling = (
    products["cost_price"] >= products["selling_price"]
).sum()

print(f"Invalid cost prices: {invalid_cost_price}")
print(f"Invalid selling prices: {invalid_selling_price}")
print(f"Cost price >= selling price: {cost_greater_than_selling}")

# --------------------------------------------------
# 6. ORDER DATA VALIDATION
# --------------------------------------------------

print("\n" + "=" * 70)
print("6. ORDER DATA VALIDATION")
print("=" * 70)

orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)

invalid_order_dates = orders["order_date"].isnull().sum()

invalid_discount = (
    (orders["discount"] < 0) |
    (orders["discount"] > 100)
).sum()

print(f"Invalid order dates: {invalid_order_dates}")
print(f"Invalid discounts: {invalid_discount}")

print(
    f"Order date range: "
    f"{orders['order_date'].min().date()} "
    f"to "
    f"{orders['order_date'].max().date()}"
)

print("\nOrder statuses:")
print(orders["status"].value_counts())

print("\nPayment methods:")
print(orders["payment_method"].value_counts())

# --------------------------------------------------
# 7. ORDER ITEM VALIDATION
# --------------------------------------------------

print("\n" + "=" * 70)
print("7. ORDER ITEM VALIDATION")
print("=" * 70)

invalid_quantity = (order_items["quantity"] <= 0).sum()
invalid_unit_price = (order_items["unit_price"] <= 0).sum()

print(f"Invalid quantities: {invalid_quantity}")
print(f"Invalid unit prices: {invalid_unit_price}")

# --------------------------------------------------
# 8. REFERENTIAL INTEGRITY
# --------------------------------------------------

print("\n" + "=" * 70)
print("8. REFERENTIAL INTEGRITY CHECK")
print("=" * 70)

invalid_order_customers = (
    ~orders["customer_id"].isin(customers["customer_id"])
).sum()

invalid_item_orders = (
    ~order_items["order_id"].isin(orders["order_id"])
).sum()

invalid_item_products = (
    ~order_items["product_id"].isin(products["product_id"])
).sum()

print(f"Orders with invalid customer IDs: {invalid_order_customers}")
print(f"Order items with invalid order IDs: {invalid_item_orders}")
print(f"Order items with invalid product IDs: {invalid_item_products}")

# --------------------------------------------------
# 9. ORDERS WITHOUT VALID ORDER ITEMS
# --------------------------------------------------

print("\n" + "=" * 70)
print("9. ORDERS WITHOUT VALID ORDER ITEMS")
print("=" * 70)

orders_with_items = order_items["order_id"].unique()

orders_without_items = orders[
    ~orders["order_id"].isin(orders_with_items)
]

print(
    f"Orders without valid order items: "
    f"{len(orders_without_items)}"
)

if len(orders_without_items) > 0:
    print("\nThese orders remain in the orders table,")
    print("but they should not contribute to sales revenue.")
else:
    print("Every order has at least one valid order item.")

# --------------------------------------------------
# 10. FINAL VALIDATION SUMMARY
# --------------------------------------------------

print("\n" + "=" * 70)
print("10. FINAL VALIDATION SUMMARY")
print("=" * 70)

checks = {
    "No missing customer ages":
        customers["age"].isnull().sum() == 0,

    "No duplicate customer IDs":
        customers["customer_id"].duplicated().sum() == 0,

    "No invalid ages":
        invalid_age == 0,

    "No city formatting issues":
        city_format_issues == 0,

    "No invalid product prices":
        invalid_cost_price == 0 and invalid_selling_price == 0,

    "Cost price < selling price":
        cost_greater_than_selling == 0,

    "No invalid order dates":
        invalid_order_dates == 0,

    "No missing payment methods":
        orders["payment_method"].isnull().sum() == 0,

    "No invalid discounts":
        invalid_discount == 0,

    "No invalid quantities":
        invalid_quantity == 0,

    "No invalid unit prices":
        invalid_unit_price == 0,

    "Valid customer relationships":
        invalid_order_customers == 0,

    "Valid order relationships":
        invalid_item_orders == 0,

    "Valid product relationships":
        invalid_item_products == 0,
}

all_passed = True

for check_name, result in checks.items():
    status = "PASS" if result else "FAIL"

    print(f"[{status}] {check_name}")

    if not result:
        all_passed = False

print("\n" + "=" * 70)

if all_passed:
    print("ALL CRITICAL VALIDATION CHECKS PASSED!")
else:
    print("SOME VALIDATION CHECKS FAILED.")
    print("Review the results above.")

print("=" * 70)