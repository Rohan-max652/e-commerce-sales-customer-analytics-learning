import pandas as pd

# ==========================================
# LOAD DATA
# ==========================================

customers = pd.read_csv("data/raw/customers.csv")
products = pd.read_csv("data/raw/products.csv")
orders = pd.read_csv("data/raw/orders.csv")
order_items = pd.read_csv("data/raw/order_items.csv")


# ==========================================
# 1. CHECK CUSTOMER DATA
# ==========================================

print("\n" + "=" * 60)
print("CUSTOMER DATA QUALITY")
print("=" * 60)

print("\nAge Statistics:")
print(customers["age"].describe())

print("\nUnique Genders:")
print(customers["gender"].value_counts(dropna=False))

print("\nCustomer States:")
print(customers["state"].value_counts())

print("\nSignup Date Range:")
print(customers["signup_date"].min(), "to", customers["signup_date"].max())


# ==========================================
# 2. CHECK PRODUCT DATA
# ==========================================

print("\n" + "=" * 60)
print("PRODUCT DATA QUALITY")
print("=" * 60)

print("\nProduct Categories:")
print(products["category"].value_counts())

print("\nProduct Brands:")
print(products["brand"].nunique())

print("\nPrice Statistics:")
print(products[["cost_price", "selling_price"]].describe())

print("\nProducts with invalid prices:")

invalid_products = products[
    (products["cost_price"] <= 0) |
    (products["selling_price"] <= 0)
]

print(len(invalid_products))


# ==========================================
# 3. CHECK ORDER DATA
# ==========================================

print("\n" + "=" * 60)
print("ORDER DATA QUALITY")
print("=" * 60)

print("\nPayment Methods:")
print(orders["payment_method"].value_counts(dropna=False))

print("\nOrder Status:")
print(orders["status"].value_counts())

print("\nDiscount Values:")
print(orders["discount"].value_counts().sort_index())

print("\nOrder Date Range:")
print(orders["order_date"].min(), "to", orders["order_date"].max())

print("\nInvalid Discounts:")

invalid_discounts = orders[
    (orders["discount"] < 0) |
    (orders["discount"] > 100)
]

print(len(invalid_discounts))


# ==========================================
# 4. CHECK ORDER ITEMS
# ==========================================

print("\n" + "=" * 60)
print("ORDER ITEMS DATA QUALITY")
print("=" * 60)

print("\nQuantity Statistics:")
print(order_items["quantity"].describe())

print("\nInvalid Quantities:")

invalid_quantities = order_items[
    order_items["quantity"] <= 0
]

print(len(invalid_quantities))

print("\nUnit Price Statistics:")
print(order_items["unit_price"].describe())

print("\nInvalid Unit Prices:")

invalid_unit_prices = order_items[
    order_items["unit_price"] <= 0
]

print(len(invalid_unit_prices))


# ==========================================
# 5. CHECK RELATIONSHIPS
# ==========================================

print("\n" + "=" * 60)
print("RELATIONSHIP VALIDATION")
print("=" * 60)


# Orders -> Customers

invalid_customer_ids = orders[
    ~orders["customer_id"].isin(customers["customer_id"])
]

print("\nOrders with invalid customer IDs:")
print(len(invalid_customer_ids))


# Order Items -> Orders

invalid_order_ids = order_items[
    ~order_items["order_id"].isin(orders["order_id"])
]

print("\nOrder Items with invalid order IDs:")
print(len(invalid_order_ids))


# Order Items -> Products

invalid_product_ids = order_items[
    ~order_items["product_id"].isin(products["product_id"])
]

print("\nOrder Items with invalid product IDs:")
print(len(invalid_product_ids))


# ==========================================
# FINAL MESSAGE
# ==========================================

print("\n" + "=" * 60)
print("DATA QUALITY CHECK COMPLETED")
print("=" * 60)


# ==========================================
# 6. INVESTIGATE DATA QUALITY ISSUES
# ==========================================

print("\n" + "=" * 60)
print("DETAILED DATA QUALITY INVESTIGATION")
print("=" * 60)


# ------------------------------------------
# Customer duplicates
# ------------------------------------------

print("\nDuplicate Customer IDs:")

duplicate_customer_ids = customers[
    customers.duplicated(
        subset="customer_id",
        keep=False
    )
].sort_values("customer_id")

print(duplicate_customer_ids.head(10))


# ------------------------------------------
# Missing customer ages
# ------------------------------------------

print("\nCustomers with Missing Age:")

missing_age_customers = customers[
    customers["age"].isnull()
]

print(missing_age_customers.head(10))


# ------------------------------------------
# Missing payment methods
# ------------------------------------------

print("\nOrders with Missing Payment Method:")

missing_payment_orders = orders[
    orders["payment_method"].isnull()
]

print(missing_payment_orders.head(10))


# ------------------------------------------
# Invalid quantities
# ------------------------------------------

print("\nOrders Items with Invalid Quantity:")

invalid_quantity_items = order_items[
    order_items["quantity"] <= 0
]

print(invalid_quantity_items.head(10))


# ------------------------------------------
# City formatting
# ------------------------------------------

print("\nUnique City Values:")

print(
    customers["city"]
    .value_counts()
    .head(30)
)


# ------------------------------------------
# Check product price relationship
# ------------------------------------------

print("\nProducts where Cost Price >= Selling Price:")

invalid_price_relationship = products[
    products["cost_price"] >= products["selling_price"]
]

print(len(invalid_price_relationship))


# ==========================================
# 7. FINAL INVESTIGATION BEFORE CLEANING
# ==========================================

print("\n" + "=" * 60)
print("FINAL INVESTIGATION")
print("=" * 60)


# ------------------------------------------
# Check city formatting variations
# ------------------------------------------

print("\nCities with possible formatting variations:")

city_check = (
    customers["city"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.lower()
    .value_counts()
)

print(city_check)


# ------------------------------------------
# Orders affected by invalid quantities
# ------------------------------------------

invalid_order_ids = (
    order_items.loc[
        order_items["quantity"] <= 0,
        "order_id"
    ]
    .unique()
)

print("\nNumber of orders containing invalid quantities:")
print(len(invalid_order_ids))


print("\nAffected Order IDs:")
print(invalid_order_ids[:20])


# ------------------------------------------
# Check whether affected orders have
# other valid order items
# ------------------------------------------

affected_items = order_items[
    order_items["order_id"].isin(invalid_order_ids)
]

valid_items_in_affected_orders = affected_items[
    affected_items["quantity"] > 0
]

print("\nInvalid order-item records:")
print(len(affected_items[affected_items["quantity"] <= 0]))

print("\nValid order-item records belonging to affected orders:")
print(len(valid_items_in_affected_orders))


# ------------------------------------------
# Check orders that would have NO valid
# order items after removing invalid rows
# ------------------------------------------

valid_order_ids = set(
    order_items.loc[
        order_items["quantity"] > 0,
        "order_id"
    ]
)

orders_without_valid_items = orders[
    ~orders["order_id"].isin(valid_order_ids)
]

print("\nOrders with no valid order items:")
print(len(orders_without_valid_items))

print("\nSample:")
print(orders_without_valid_items.head(10))


# ==========================================
# 8. CONFIRM CITY FORMAT INCONSISTENCIES
# ==========================================

print("\n" + "=" * 60)
print("CITY FORMAT INCONSISTENCY CHECK")
print("=" * 60)

# Group original city values after normalizing case
city_groups = (
    customers.groupby(
        customers["city"].astype(str).str.strip().str.lower()
    )["city"]
    .unique()
)

# Show only cities that have more than one original format
city_variations = city_groups[
    city_groups.apply(len) > 1
]

print("\nCities with multiple original formats:")

if len(city_variations) == 0:
    print("No formatting inconsistencies found.")
else:
    for normalized_city, variations in city_variations.items():
        print(f"{normalized_city} -> {list(variations)}")

print(f"\nNumber of cities with formatting variations: {len(city_variations)}")