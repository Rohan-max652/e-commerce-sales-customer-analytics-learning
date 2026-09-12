import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# E-COMMERCE SALES & CUSTOMER ANALYTICS
# Dataset Generation Script
# ============================================================

# -----------------------------
# 1. Project configuration
# -----------------------------

np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# Number of records
NUM_CUSTOMERS = 10_000
NUM_PRODUCTS = 1_000
NUM_ORDERS = 50_000


# -----------------------------
# 2. Customer data
# -----------------------------

first_names = [
    "Aarav", "Aditi", "Arjun", "Ananya", "Aditya",
    "Ishaan", "Isha", "Rahul", "Riya", "Rohan",
    "Priya", "Neha", "Sneha", "Pooja", "Karan",
    "Vivek", "Nisha", "Soham", "Sayan", "Moumita",
    "Anirban", "Ritwik", "Sourav", "Debanjan", "Tania",
    "Raj", "Simran", "Kavya", "Meera", "Manish"
]

last_names = [
    "Sharma", "Das", "Roy", "Sen", "Banerjee",
    "Mukherjee", "Chatterjee", "Bose", "Dutta", "Ghosh",
    "Patel", "Shah", "Gupta", "Verma", "Singh",
    "Kumar", "Mehta", "Nair", "Iyer", "Reddy"
]

locations = {
    "West Bengal": ["Kolkata", "Siliguri", "Durgapur", "Asansol", "Howrah"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Thane"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru", "Hubli", "Belagavi"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli"],
    "Delhi": ["New Delhi", "Delhi"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Noida"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela"],
    "Kerala": ["Kochi", "Thiruvananthapuram", "Kozhikode"]
}

states = list(locations.keys())

customer_rows = []

for i in range(1, NUM_CUSTOMERS + 1):
    state = np.random.choice(states)
    city = np.random.choice(locations[state])

    first_name = np.random.choice(first_names)
    last_name = np.random.choice(last_names)

    name = f"{first_name} {last_name}"

    gender = np.random.choice(
        ["Male", "Female"],
        p=[0.52, 0.48]
    )

    age = np.random.randint(18, 61)

    signup_date = pd.Timestamp("2023-01-01") + pd.Timedelta(
        days=int(np.random.randint(0, 1095))
    )

    customer_rows.append([
        i,
        name,
        gender,
        age,
        city,
        state,
        signup_date
    ])

customers = pd.DataFrame(
    customer_rows,
    columns=[
        "customer_id",
        "name",
        "gender",
        "age",
        "city",
        "state",
        "signup_date"
    ]
)


# -----------------------------
# 3. Product data
# -----------------------------

product_categories = {
    "Electronics": [
        "Smartphone", "Laptop", "Tablet", "Smartwatch",
        "Headphones", "Bluetooth Speaker", "Monitor",
        "Keyboard", "Mouse", "Power Bank"
    ],
    "Fashion": [
        "T-Shirt", "Jeans", "Kurta", "Saree",
        "Jacket", "Shoes", "Sandals", "Handbag",
        "Backpack", "Watch"
    ],
    "Home & Kitchen": [
        "Mixer Grinder", "Cookware Set", "Bedsheet",
        "Curtains", "Dining Set", "Water Bottle",
        "Storage Box", "Air Fryer", "Coffee Maker", "Lamp"
    ],
    "Beauty & Personal Care": [
        "Face Wash", "Moisturizer", "Shampoo",
        "Perfume", "Lipstick", "Sunscreen",
        "Hair Dryer", "Body Lotion", "Face Serum", "Trimmer"
    ],
    "Sports": [
        "Cricket Bat", "Football", "Badminton Racket",
        "Yoga Mat", "Dumbbells", "Running Shoes",
        "Sports Bag", "Tennis Ball", "Cycling Helmet", "Skipping Rope"
    ],
    "Books": [
        "Novel", "Programming Book", "Business Book",
        "Self Help Book", "Exam Preparation Book",
        "Biography", "History Book", "Science Book",
        "Finance Book", "Children Book"
    ],
    "Grocery": [
        "Rice", "Atta", "Cooking Oil", "Tea",
        "Coffee", "Biscuits", "Spices", "Dry Fruits",
        "Cereals", "Snacks"
    ]
}

category_price_ranges = {
    "Electronics": (500, 80000),
    "Fashion": (300, 8000),
    "Home & Kitchen": (200, 15000),
    "Beauty & Personal Care": (150, 5000),
    "Sports": (250, 12000),
    "Books": (100, 2500),
    "Grocery": (50, 3000)
}

brands = [
    "Nova", "UrbanKart", "Prime", "Elite",
    "DailyChoice", "TechPro", "StyleHub",
    "HomePlus", "FitLife", "SmartBuy",
    "FreshMart", "Trendify"
]

product_rows = []

for i in range(1, NUM_PRODUCTS + 1):

    category = np.random.choice(list(product_categories.keys()))

    product_type = np.random.choice(product_categories[category])
    brand = np.random.choice(brands)

    product_name = f"{brand} {product_type}"

    min_price, max_price = category_price_ranges[category]

    selling_price = round(
        np.random.uniform(min_price, max_price),
        2
    )

    cost_price = round(
        selling_price * np.random.uniform(0.55, 0.85),
        2
    )

    product_rows.append([
        i,
        product_name,
        category,
        brand,
        cost_price,
        selling_price
    ])

products = pd.DataFrame(
    product_rows,
    columns=[
        "product_id",
        "product_name",
        "category",
        "brand",
        "cost_price",
        "selling_price"
    ]
)


# -----------------------------
# 4. Order data
# -----------------------------

customer_ids = np.arange(1, NUM_CUSTOMERS + 1)

# Give some customers a higher probability of ordering.
# This naturally creates repeat customers.
customer_weights = np.random.exponential(
    scale=1.0,
    size=NUM_CUSTOMERS
)

customer_weights = customer_weights / customer_weights.sum()

order_customer_ids = np.random.choice(
    customer_ids,
    size=NUM_ORDERS,
    p=customer_weights
)

order_dates = pd.to_datetime(
    np.random.choice(
        pd.date_range("2024-01-01", "2026-08-31"),
        size=NUM_ORDERS
    )
)

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery",
    "Wallet"
]

statuses = [
    "Delivered",
    "Delivered",
    "Delivered",
    "Delivered",
    "Shipped",
    "Cancelled",
    "Returned"
]

order_rows = []

for i in range(1, NUM_ORDERS + 1):

    customer_id = order_customer_ids[i - 1]
    order_date = order_dates[i - 1]

    payment_method = np.random.choice(
        payment_methods,
        p=[0.38, 0.20, 0.15, 0.08, 0.12, 0.07]
    )

    discount = np.random.choice(
        [0, 5, 10, 15, 20, 25, 30],
        p=[0.18, 0.20, 0.25, 0.18, 0.12, 0.05, 0.02]
    )

    status = np.random.choice(
        statuses
    )

    order_rows.append([
        i,
        customer_id,
        order_date,
        payment_method,
        discount,
        status
    ])

orders = pd.DataFrame(
    order_rows,
    columns=[
        "order_id",
        "customer_id",
        "order_date",
        "payment_method",
        "discount",
        "status"
    ]
)


# -----------------------------
# 5. Order items
# -----------------------------

# Each order contains 1–5 products
items_per_order = np.random.choice(
    [1, 2, 3, 4, 5],
    size=NUM_ORDERS,
    p=[0.40, 0.30, 0.18, 0.08, 0.04]
)

order_item_rows = []

order_item_id = 1

for order_id, item_count in zip(
    orders["order_id"],
    items_per_order
):

    selected_products = np.random.choice(
        products["product_id"],
        size=item_count,
        replace=False
    )

    for product_id in selected_products:

        product = products.loc[
            products["product_id"] == product_id
        ].iloc[0]

        quantity = np.random.choice(
            [1, 2, 3, 4],
            p=[0.65, 0.22, 0.10, 0.03]
        )

        unit_price = product["selling_price"]

        order_item_rows.append([
            order_item_id,
            order_id,
            product_id,
            quantity,
            unit_price
        ])

        order_item_id += 1

order_items = pd.DataFrame(
    order_item_rows,
    columns=[
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price"
    ]
)


# ============================================================
# 6. Add a few realistic data-quality problems
# ============================================================

# Missing payment methods
missing_payment_indices = np.random.choice(
    orders.index,
    size=250,
    replace=False
)

orders.loc[
    missing_payment_indices,
    "payment_method"
] = np.nan


# Inconsistent city text
city_indices = np.random.choice(
    customers.index,
    size=100,
    replace=False
)

customers.loc[
    city_indices[:50],
    "city"
] = customers.loc[
    city_indices[:50],
    "city"
].str.upper()

customers.loc[
    city_indices[50:],
    "city"
] = customers.loc[
    city_indices[50:],
    "city"
].str.lower()


# A few invalid quantities
invalid_quantity_indices = np.random.choice(
    order_items.index,
    size=100,
    replace=False
)

orders_items_invalid_values = np.random.choice(
    [0, -1],
    size=100
)

order_items.loc[
    invalid_quantity_indices,
    "quantity"
] = orders_items_invalid_values


# A few missing ages
missing_age_indices = np.random.choice(
    customers.index,
    size=150,
    replace=False
)

customers.loc[
    missing_age_indices,
    "age"
] = np.nan


# Duplicate customer records
duplicate_customers = customers.sample(
    50,
    random_state=42
)

customers = pd.concat(
    [customers, duplicate_customers],
    ignore_index=True
)


# -----------------------------
# 7. Save raw datasets
# -----------------------------

customers.to_csv(
    DATA_DIR / "customers.csv",
    index=False
)

products.to_csv(
    DATA_DIR / "products.csv",
    index=False
)

orders.to_csv(
    DATA_DIR / "orders.csv",
    index=False
)

order_items.to_csv(
    DATA_DIR / "order_items.csv",
    index=False
)


# -----------------------------
# 8. Display summary
# -----------------------------

print("\n==========================================")
print("E-COMMERCE DATASET CREATED SUCCESSFULLY")
print("==========================================")

print(f"\nCustomers:   {len(customers):,}")
print(f"Products:    {len(products):,}")
print(f"Orders:      {len(orders):,}")
print(f"Order Items: {len(order_items):,}")

print("\nFiles created in:")
print(DATA_DIR)

print("\nFiles:")
print("1. customers.csv")
print("2. products.csv")
print("3. orders.csv")
print("4. order_items.csv")

print("\nDataset generation completed!")