import pandas as pd

# Load cleaned datasets
customers = pd.read_csv("data/cleaned/customers_cleaned.csv")
products = pd.read_csv("data/cleaned/products_cleaned.csv")
orders = pd.read_csv("data/cleaned/orders_cleaned.csv")
order_items = pd.read_csv("data/cleaned/order_items_cleaned.csv")

# Convert date columns
customers["signup_date"] = pd.to_datetime(customers["signup_date"])
orders["order_date"] = pd.to_datetime(orders["order_date"])

# Display dataset sizes
print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)


# Merge orders with order items
sales = orders.merge(
    order_items,
    on="order_id",
    how="inner"
)

# Merge with product information
sales = sales.merge(
    products,
    on="product_id",
    how="left"
)

# Merge with customer information
sales = sales.merge(
    customers,
    on="customer_id",
    how="left"
)

# Create calculated sales metrics
sales["revenue"] = sales["quantity"] * sales["unit_price"]

sales["profit"] = sales["quantity"] * (
    sales["unit_price"] - sales["cost_price"]
)

# Display combined dataset information
print("\nCombined Sales Dataset:")
print("Rows:", len(sales))
print("Columns:", len(sales.columns))

print("\nColumns:")
print(sales.columns.tolist())


import matplotlib.pyplot as plt

# Filter delivered orders for revenue analysis
delivered_sales = sales[sales["status"] == "Delivered"].copy()

# Create monthly revenue
monthly_revenue = (
    delivered_sales
    .groupby(delivered_sales["order_date"].dt.to_period("M"))["revenue"]
    .sum()
    .reset_index()
)

# Convert period to timestamp for plotting
monthly_revenue["order_date"] = monthly_revenue["order_date"].dt.to_timestamp()

# Display monthly revenue
print("\nMonthly Revenue:")
print(monthly_revenue)

# Create chart
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue["order_date"],
    monthly_revenue["revenue"],
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

# Save chart
plt.savefig("reports/monthly_revenue_trend.png", dpi=300)

plt.show()


# =========================================================
# MONTHLY PROFIT TREND
# =========================================================

monthly_profit = (
    delivered_sales
    .groupby(delivered_sales["order_date"].dt.to_period("M"))["profit"]
    .sum()
    .reset_index()
)

monthly_profit["order_date"] = monthly_profit["order_date"].dt.to_timestamp()

print("\nMonthly Profit:")
print(monthly_profit)

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_profit["order_date"],
    monthly_profit["profit"],
    marker="o"
)

plt.title("Monthly Profit Trend")
plt.xlabel("Month")
plt.ylabel("Profit")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "reports/monthly_profit_trend.png",
    dpi=300
)

# -----------------------------------------
# 4. Category Revenue & Profit Analysis
# -----------------------------------------

category_summary = (
    sales.groupby("category")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum")
    )
    .sort_values("revenue", ascending=False)
)

plt.figure(figsize=(10, 6))
plt.bar(category_summary.index, category_summary["revenue"])

plt.title("Revenue by Product Category")
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "reports/category_revenue.png",
    dpi=300
)

plt.show()


# =========================================================
# TOP 10 PRODUCTS BY REVENUE
# =========================================================

top_products = (
    delivered_sales
    .groupby("product_name")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Products by Revenue:")
print(top_products)

plt.figure(figsize=(10, 6))

plt.barh(
    top_products.index[::-1],
    top_products.values[::-1]
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    "reports/top_10_products_revenue.png",
    dpi=300
)

plt.show()


# =========================================================
# TOP 10 CUSTOMERS BY REVENUE
# =========================================================

top_customers = (
    delivered_sales
    .groupby(["customer_id", "customer_name"])["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Customers by Revenue:")
print(top_customers)

plt.figure(figsize=(10, 6))

plt.barh(
    top_customers.index.get_level_values("customer_name")[::-1],
    top_customers.values[::-1]
)

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Customer")

plt.tight_layout()

plt.savefig(
    "reports/top_10_customers_revenue.png",
    dpi=300
)

plt.show()


# =========================================================
# ORDER STATUS DISTRIBUTION
# =========================================================

status_counts = orders["status"].value_counts()

print("\nOrder Status Distribution:")
print(status_counts)

plt.figure(figsize=(8, 6))

plt.bar(
    status_counts.index,
    status_counts.values
)

plt.title("Order Status Distribution")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")

plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    "reports/order_status_distribution.png",
    dpi=300
)

plt.show()


# =========================================================
# REVENUE BY PAYMENT METHOD
# =========================================================

payment_revenue = (
    delivered_sales
    .groupby("payment_method")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRevenue by Payment Method:")
print(payment_revenue)

plt.figure(figsize=(10, 6))

plt.bar(
    payment_revenue.index,
    payment_revenue.values
)

plt.title("Revenue by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Revenue")

plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    "reports/payment_method_revenue.png",
    dpi=300
)

plt.show()


# =========================================================
# CUSTOMER AGE DISTRIBUTION
# =========================================================

age_distribution = customers["age"]

print("\nCustomer Age Statistics:")
print(age_distribution.describe())

plt.figure(figsize=(10, 6))

plt.hist(
    age_distribution,
    bins=10
)

plt.title("Customer Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    "reports/customer_age_distribution.png",
    dpi=300
)

plt.show()


# =========================================================
# REVENUE BY CUSTOMER CITY
# =========================================================

city_revenue = (
    delivered_sales
    .groupby("city")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Cities by Revenue:")
print(city_revenue)

plt.figure(figsize=(10, 6))

plt.barh(
    city_revenue.index[::-1],
    city_revenue.values[::-1]
)

plt.title("Top 10 Cities by Revenue")
plt.xlabel("Revenue")
plt.ylabel("City")

plt.tight_layout()

plt.savefig(
    "reports/top_10_cities_revenue.png",
    dpi=300
)

plt.show()


# =========================================================
# CUSTOMER GENDER DISTRIBUTION
# =========================================================

gender_counts = customers["gender"].value_counts()

print("\nCustomer Gender Distribution:")
print(gender_counts)

plt.figure(figsize=(8, 6))

plt.bar(
    gender_counts.index,
    gender_counts.values
)

plt.title("Customer Gender Distribution")
plt.xlabel("Gender")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    "reports/customer_gender_distribution.png",
    dpi=300
)

plt.show()


# =========================================================
# CUSTOMER AGE GROUP ANALYSIS
# =========================================================

customers["age_group"] = pd.cut(
    customers["age"],
    bins=[17, 25, 35, 45, 55, 60],
    labels=["18-25", "26-35", "36-45", "46-55", "56-60"]
)

age_group_counts = customers["age_group"].value_counts().sort_index()

print("\nCustomer Age Group Distribution:")
print(age_group_counts)

plt.figure(figsize=(9, 6))

plt.bar(
    age_group_counts.index.astype(str),
    age_group_counts.values
)

plt.title("Customer Age Group Distribution")
plt.xlabel("Age Group")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    "reports/customer_age_group_distribution.png",
    dpi=300
)

plt.show()


# =========================================================
# REVENUE BY CUSTOMER AGE GROUP
# =========================================================

delivered_sales["age_group"] = pd.cut(
    delivered_sales["age"],
    bins=[17, 25, 35, 45, 55, 60],
    labels=["18-25", "26-35", "36-45", "46-55", "56-60"]
)

age_group_revenue = (
    delivered_sales
    .groupby("age_group", observed=True)["revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRevenue by Customer Age Group:")
print(age_group_revenue)

plt.figure(figsize=(9, 6))

plt.bar(
    age_group_revenue.index.astype(str),
    age_group_revenue.values
)

plt.title("Revenue by Customer Age Group")
plt.xlabel("Age Group")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig(
    "reports/revenue_by_age_group.png",
    dpi=300
)

plt.show()


# =========================================================
# AVERAGE ORDER VALUE BY CUSTOMER
# =========================================================

customer_order_value = (
    delivered_sales
    .groupby(["customer_id", "order_id"])["revenue"]
    .sum()
    .reset_index()
)

aov_summary = (
    customer_order_value["revenue"]
    .agg(["mean", "median", "min", "max"])
)

print("\nCustomer Order Value Statistics:")
print(aov_summary)


# =========================================================
# REVENUE BY CUSTOMER GENDER
# =========================================================

gender_revenue = (
    delivered_sales
    .groupby("gender")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRevenue by Customer Gender:")
print(gender_revenue)

plt.figure(figsize=(8, 6))

plt.bar(
    gender_revenue.index,
    gender_revenue.values
)

plt.title("Revenue by Customer Gender")
plt.xlabel("Gender")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig(
    "reports/revenue_by_gender.png",
    dpi=300
)

plt.show()


# =========================================================
# ORDER VALUE DISTRIBUTION
# =========================================================

plt.figure(figsize=(10, 6))

plt.hist(
    customer_order_value["revenue"],
    bins=50
)

plt.title("Order Value Distribution")
plt.xlabel("Order Value")
plt.ylabel("Number of Orders")

plt.tight_layout()

plt.savefig(
    "reports/order_value_distribution.png",
    dpi=300
)

plt.show()


# =========================================================
# PROFIT BY PRODUCT CATEGORY
# =========================================================

category_profit = (
    delivered_sales
    .groupby("category")["profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\nProfit by Product Category:")
print(category_profit)

plt.figure(figsize=(10, 6))

plt.bar(
    category_profit.index,
    category_profit.values
)

plt.title("Profit by Product Category")
plt.xlabel("Category")
plt.ylabel("Profit")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "reports/category_profit.png",
    dpi=300
)

plt.show()


# =========================================================
# PROFIT MARGIN BY PRODUCT CATEGORY
# =========================================================

category_margin = (
    delivered_sales
    .groupby("category")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum")
    )
)

category_margin["profit_margin_percent"] = (
    category_margin["profit"]
    / category_margin["revenue"]
    * 100
)

category_margin = category_margin.sort_values(
    "profit_margin_percent",
    ascending=False
)

print("\nProfit Margin by Product Category:")
print(category_margin)

plt.figure(figsize=(10, 6))

plt.bar(
    category_margin.index,
    category_margin["profit_margin_percent"]
)

plt.title("Profit Margin by Product Category")
plt.xlabel("Category")
plt.ylabel("Profit Margin (%)")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "reports/category_profit_margin.png",
    dpi=300
)

plt.show()


# =========================================================
# TOP 10 PRODUCTS BY PROFIT
# =========================================================

top_products_profit = (
    delivered_sales
    .groupby("product_name")["profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Products by Profit:")
print(top_products_profit)

plt.figure(figsize=(10, 6))

plt.barh(
    top_products_profit.index[::-1],
    top_products_profit.values[::-1]
)

plt.title("Top 10 Products by Profit")
plt.xlabel("Profit")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    "reports/top_10_products_profit.png",
    dpi=300
)

plt.show()


# =========================================================
# TOP 10 PRODUCTS BY QUANTITY SOLD
# =========================================================

top_products_quantity = (
    delivered_sales
    .groupby("product_name")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Products by Quantity Sold:")
print(top_products_quantity)

plt.figure(figsize=(10, 6))

plt.barh(
    top_products_quantity.index[::-1],
    top_products_quantity.values[::-1]
)

plt.title("Top 10 Products by Quantity Sold")
plt.xlabel("Quantity Sold")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    "reports/top_10_products_quantity.png",
    dpi=300
)

plt.show()


# =========================================================
# CUSTOMER PURCHASE FREQUENCY
# =========================================================

customer_orders = (
    delivered_sales
    .groupby("customer_id")["order_id"]
    .nunique()
    .sort_values(ascending=False)
)

print("\nCustomer Purchase Frequency:")
print(customer_orders.describe())

# Customer frequency groups
frequency_groups = pd.cut(
    customer_orders,
    bins=[0, 1, 3, 5, float("inf")],
    labels=["1 Order", "2-3 Orders", "4-5 Orders", "6+ Orders"]
)

frequency_distribution = frequency_groups.value_counts().sort_index()

print("\nCustomer Frequency Distribution:")
print(frequency_distribution)

plt.figure(figsize=(10, 6))

plt.bar(
    frequency_distribution.index,
    frequency_distribution.values
)

plt.title("Customer Purchase Frequency")
plt.xlabel("Number of Orders")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    "reports/customer_purchase_frequency.png",
    dpi=300
)

plt.show()


# =========================================================
# RFM CUSTOMER SEGMENTATION
# =========================================================

# Reference date = day after the latest delivered order
reference_date = delivered_sales["order_date"].max() + pd.Timedelta(days=1)

rfm = (
    delivered_sales
    .groupby("customer_id")
    .agg(
        Recency=("order_date", lambda x: (reference_date - x.max()).days),
        Frequency=("order_id", "nunique"),
        Monetary=("revenue", "sum")
    )
    .reset_index()
)

print("\nRFM Customer Analysis:")
print(rfm.head())

print("\nRFM Statistics:")
print(rfm[["Recency", "Frequency", "Monetary"]].describe())


# =========================================================
# RFM SCORING
# =========================================================

# Recency:
# Lower recency is better, so scoring is reversed.
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

# Frequency:
# Higher frequency is better.
rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Monetary:
# Higher monetary value is better.
rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Combined RFM score
rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)

print("\nRFM Scoring:")
print(rfm.head(10))

print("\nRFM Score Distribution:")
print(rfm["RFM_Score"].value_counts().head(20))


# =========================================================
# CUSTOMER SEGMENTS
# =========================================================

def assign_segment(row):
    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    # Highest-value customers
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    # Frequent and valuable customers
    elif r >= 3 and f >= 4 and m >= 3:
        return "Loyal Customers"

    # Recent customers with growth potential
    elif r >= 4 and f <= 3 and m >= 2:
        return "Potential Loyalists"

    # Previously valuable/frequent but not recently active
    elif r <= 2 and f >= 3 and m >= 3:
        return "At Risk"

    # Low engagement customers
    elif r <= 2 and f <= 2 and m <= 2:
        return "Lost Customers"

    else:
        return "Others"


rfm["Segment"] = rfm.apply(assign_segment, axis=1)

print("\nCustomer Segment Distribution:")
print(rfm["Segment"].value_counts())

print("\nCustomer Segment Summary:")
segment_summary = (
    rfm.groupby("Segment")
    .agg(
        Customers=("customer_id", "count"),
        Avg_Recency=("Recency", "mean"),
        Avg_Frequency=("Frequency", "mean"),
        Total_Revenue=("Monetary", "sum"),
        Avg_Revenue=("Monetary", "mean")
    )
    .sort_values("Total_Revenue", ascending=False)
)

print(segment_summary)


# =========================================================
# RFM SEGMENT DISTRIBUTION
# =========================================================

segment_counts = (
    rfm["Segment"]
    .value_counts()
)

plt.figure(figsize=(10, 6))

plt.bar(
    segment_counts.index,
    segment_counts.values
)

plt.title("Customer Segment Distribution")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "reports/customer_segments.png",
    dpi=300
)

plt.show()


# =========================================================
# REVENUE BY CUSTOMER SEGMENT
# =========================================================

segment_revenue = (
    rfm.groupby("Segment")["Monetary"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))

plt.bar(
    segment_revenue.index,
    segment_revenue.values
)

plt.title("Revenue by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Revenue")
plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "reports/revenue_by_customer_segment.png",
    dpi=300
)

plt.show()