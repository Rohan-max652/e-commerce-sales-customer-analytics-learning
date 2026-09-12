import pandas as pd

# ============================================================
# LOAD CLEANED DATA
# ============================================================

customers = pd.read_csv("data/cleaned/customers_cleaned.csv")
products = pd.read_csv("data/cleaned/products_cleaned.csv")
orders = pd.read_csv("data/cleaned/orders_cleaned.csv")
order_items = pd.read_csv("data/cleaned/order_items_cleaned.csv")

orders["order_date"] = pd.to_datetime(orders["order_date"])

# ============================================================
# MERGE DATA
# ============================================================

sales = (
    order_items
    .merge(orders, on="order_id", how="left")
    .merge(products, on="product_id", how="left")
    .merge(customers, on="customer_id", how="left")
)

sales["revenue"] = sales["quantity"] * sales["unit_price"]

sales["profit"] = (
    sales["quantity"] *
    (sales["unit_price"] - sales["cost_price"])
)

delivered = sales[sales["status"] == "Delivered"].copy()

# ============================================================
# 1. OVERALL KPIs
# ============================================================

total_revenue = delivered["revenue"].sum()
total_profit = delivered["profit"].sum()
profit_margin = total_profit / total_revenue * 100
delivered_orders = delivered["order_id"].nunique()
aov = total_revenue / delivered_orders

print("\n========== FINAL BUSINESS INSIGHTS ==========\n")

print("Overall Performance")
print(f"Revenue: Rs.{total_revenue:,.2f}")
print(f"Profit: Rs.{total_profit:,.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")
print(f"Delivered Orders: {delivered_orders:,}")
print(f"Average Order Value: Rs.{aov:,.2f}")

# ============================================================
# 2. TOP CATEGORY
# ============================================================

category = (
    delivered
    .groupby("category")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        units=("quantity", "sum")
    )
    .sort_values("revenue", ascending=False)
)

print("\nTop Categories")
print(category.round(2))

# ============================================================
# 3. TOP STATES
# ============================================================

state = (
    delivered
    .groupby("state")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique")
    )
    .sort_values("revenue", ascending=False)
)

print("\nTop States by Revenue")
print(state.head(5).round(2))

# ============================================================
# 4. TOP PRODUCTS
# ============================================================

product = (
    delivered
    .groupby(["product_id", "product_name"])
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        units=("quantity", "sum")
    )
    .sort_values("revenue", ascending=False)
)

print("\nTop 10 Products by Revenue")
print(product.head(10).round(2))

# ============================================================
# 5. PAYMENT METHODS
# ============================================================

payment = (
    delivered
    .groupby("payment_method")
    .agg(
        revenue=("revenue", "sum"),
        orders=("order_id", "nunique")
    )
    .sort_values("revenue", ascending=False)
)

print("\nPayment Method Performance")
print(payment.round(2))

# ============================================================
# 6. CUSTOMER SEGMENTATION SUMMARY
# ============================================================

customer_orders = (
    delivered
    .groupby("customer_id")
    .agg(
        orders=("order_id", "nunique"),
        revenue=("revenue", "sum"),
        profit=("profit", "sum")
    )
)

print("\nCustomer Purchase Summary")
print(customer_orders.describe().round(2))

print("\n==============================================")
print("FINAL BUSINESS INSIGHTS COMPLETED")
print("==============================================")