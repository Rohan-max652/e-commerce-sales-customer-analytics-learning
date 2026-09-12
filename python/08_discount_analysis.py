import pandas as pd
import numpy as np

# ============================================================
# LOAD CLEANED DATA
# ============================================================

customers = pd.read_csv("data/cleaned/customers_cleaned.csv")
products = pd.read_csv("data/cleaned/products_cleaned.csv")
orders = pd.read_csv("data/cleaned/orders_cleaned.csv")
order_items = pd.read_csv("data/cleaned/order_items_cleaned.csv")

# Convert date
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

# ============================================================
# CALCULATE REVENUE AND PROFIT
# ============================================================

sales["revenue"] = sales["quantity"] * sales["unit_price"]

sales["profit"] = (
    sales["quantity"] *
    (sales["unit_price"] - sales["cost_price"])
)

# Only delivered sales
delivered_sales = sales[
    sales["status"] == "Delivered"
].copy()

# ============================================================
# CREATE DISCOUNT BANDS
# ============================================================

bins = [-0.01, 5, 10, 15, 20, 25, 30]
labels = [
    "0-5%",
    "5-10%",
    "10-15%",
    "15-20%",
    "20-25%",
    "25-30%"
]

delivered_sales["discount_band"] = pd.cut(
    delivered_sales["discount"],
    bins=bins,
    labels=labels
)

# ============================================================
# DISCOUNT IMPACT ANALYSIS
# ============================================================

discount_analysis = (
    delivered_sales
    .groupby("discount_band", observed=True)
    .agg(
        orders=("order_id", "nunique"),
        units_sold=("quantity", "sum"),
        revenue=("revenue", "sum"),
        profit=("profit", "sum")
    )
)

discount_analysis["average_order_value"] = (
    discount_analysis["revenue"] /
    discount_analysis["orders"]
)

discount_analysis["profit_margin_percent"] = (
    discount_analysis["profit"] /
    discount_analysis["revenue"] * 100
)

print("\n========== DISCOUNT IMPACT ANALYSIS ==========\n")
print(discount_analysis.round(2))

# ============================================================
# AVERAGE VALUES BY DISCOUNT BAND
# ============================================================

average_discount_analysis = (
    delivered_sales
    .groupby("discount_band", observed=True)
    .agg(
        avg_discount=("discount", "mean"),
        avg_revenue_per_item=("revenue", "mean"),
        avg_units_per_item=("quantity", "mean"),
        avg_profit_per_item=("profit", "mean")
    )
)

print("\n========== AVERAGE METRICS BY DISCOUNT BAND ==========\n")
print(average_discount_analysis.round(2))

# ============================================================
# CORRELATION
# ============================================================

correlation = delivered_sales[
    ["discount", "quantity", "revenue", "profit"]
].corr()

print("\n========== DISCOUNT CORRELATION ==========\n")
print(correlation.round(3))

print("\n========== DISCOUNT ANALYSIS COMPLETED ==========")