import pandas as pd

# =========================================================
# 1. LOAD DATA
# =========================================================

customers = pd.read_csv("data/cleaned/customers_cleaned.csv")
products = pd.read_csv("data/cleaned/products_cleaned.csv")
orders = pd.read_csv("data/cleaned/orders_cleaned.csv")
order_items = pd.read_csv("data/cleaned/order_items_cleaned.csv")


# =========================================================
# 2. CONVERT DATE COLUMNS
# =========================================================

customers["signup_date"] = pd.to_datetime(customers["signup_date"])
orders["order_date"] = pd.to_datetime(orders["order_date"])


# =========================================================
# 3. CREATE ANALYSIS DATASET
# =========================================================

sales = (
    order_items
    .merge(
        orders[["order_id", "customer_id", "order_date", "status",
                "payment_method", "discount"]],
        on="order_id",
        how="left"
    )
    .merge(
        products[["product_id", "product_name", "category",
                  "brand", "cost_price"]],
        on="product_id",
        how="left"
    )
    .merge(
        customers[["customer_id", "customer_name", "city", "state"]],
        on="customer_id",
        how="left"
    )
)

# Only delivered orders are treated as realized sales
delivered_sales = sales[sales["status"] == "Delivered"].copy()


# =========================================================
# 4. CALCULATE REVENUE AND PROFIT
# =========================================================

delivered_sales["revenue"] = (
    delivered_sales["quantity"] *
    delivered_sales["unit_price"]
)

delivered_sales["cost"] = (
    delivered_sales["quantity"] *
    delivered_sales["cost_price"]
)

delivered_sales["profit"] = (
    delivered_sales["revenue"] -
    delivered_sales["cost"]
)


# =========================================================
# 5. KEY BUSINESS KPIs
# =========================================================

total_revenue = delivered_sales["revenue"].sum()
total_profit = delivered_sales["profit"].sum()

delivered_orders = delivered_sales["order_id"].nunique()

profit_margin = (
    total_profit / total_revenue * 100
)

average_order_value = (
    total_revenue / delivered_orders
)


print("\n========== KEY BUSINESS KPIs ==========")

print(f"Delivered Orders : {delivered_orders:,}")
print(f"Total Revenue    : ₹{total_revenue:,.2f}")
print(f"Total Profit     : ₹{total_profit:,.2f}")
print(f"Profit Margin    : {profit_margin:.2f}%")
print(f"Average Order Value : ₹{average_order_value:,.2f}")


# =========================================================
# 6. MONTHLY REVENUE
# =========================================================

monthly_sales = (
    delivered_sales
    .groupby(
        delivered_sales["order_date"].dt.to_period("M")
    )
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique")
    )
    .reset_index()
)

monthly_sales["order_date"] = (
    monthly_sales["order_date"].astype(str)
)

monthly_sales["profit_margin_percent"] = (
    monthly_sales["profit"] /
    monthly_sales["revenue"] * 100
)

print("\n========== MONTHLY SALES ==========")

print(monthly_sales.to_string(index=False))


# =========================================================
# 7. CATEGORY PERFORMANCE
# =========================================================

category_sales = (
    delivered_sales
    .groupby("category")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        units_sold=("quantity", "sum")
    )
    .sort_values("revenue", ascending=False)
)

category_sales["profit_margin_percent"] = (
    category_sales["profit"] /
    category_sales["revenue"] * 100
)

print("\n========== CATEGORY PERFORMANCE ==========")

print(category_sales)


# =========================================================
# 8. STATE PERFORMANCE
# =========================================================

state_sales = (
    delivered_sales
    .groupby("state")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        delivered_orders=("order_id", "nunique")
    )
    .sort_values("revenue", ascending=False)
)

print("\n========== STATE PERFORMANCE ==========")

print(state_sales)


# =========================================================
# 9. TOP 10 PRODUCTS
# =========================================================

top_products = (
    delivered_sales
    .groupby(
        ["product_id", "product_name", "category"]
    )
    .agg(
        units_sold=("quantity", "sum"),
        revenue=("revenue", "sum"),
        profit=("profit", "sum")
    )
    .sort_values("revenue", ascending=False)
    .head(10)
)

print("\n========== TOP 10 PRODUCTS ==========")

print(top_products)


# =========================================================
# 10. TOP 10 CUSTOMERS
# =========================================================

top_customers = (
    delivered_sales
    .groupby(
        ["customer_id", "customer_name"]
    )
    .agg(
        orders=("order_id", "nunique"),
        revenue=("revenue", "sum"),
        profit=("profit", "sum")
    )
    .sort_values("revenue", ascending=False)
    .head(10)
)

print("\n========== TOP 10 CUSTOMERS ==========")

print(top_customers)


# =========================================================
# 11. ORDER STATUS ANALYSIS
# =========================================================

status_analysis = (
    orders
    .groupby("status")
    .agg(
        orders=("order_id", "count")
    )
)

status_analysis["percentage"] = (
    status_analysis["orders"] /
    len(orders) * 100
)

print("\n========== ORDER STATUS ANALYSIS ==========")

print(status_analysis)


# =========================================================
# 12. PAYMENT METHOD ANALYSIS
# =========================================================

payment_analysis = (
    delivered_sales
    .groupby("payment_method")
    .agg(
        orders=("order_id", "nunique"),
        revenue=("revenue", "sum")
    )
    .sort_values("revenue", ascending=False)
)

payment_analysis["average_order_value"] = (
    payment_analysis["revenue"] /
    payment_analysis["orders"]
)

print("\n========== PAYMENT METHOD ANALYSIS ==========")

print(payment_analysis)


print("\n========== BUSINESS ANALYSIS COMPLETED ==========")