import pandas as pd

# File locations
files = {
    "Customers": "data/raw/customers.csv",
    "Products": "data/raw/products.csv",
    "Orders": "data/raw/orders.csv",
    "Order Items": "data/raw/order_items.csv"
}

# Inspect each dataset
for name, file_path in files.items():

    print("\n" + "=" * 60)
    print(f"{name.upper()} DATASET")
    print("=" * 60)

    # Load data
    df = pd.read_csv(file_path)

    # Basic information
    print(f"\nRows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print(f"\nDuplicate Rows: {df.duplicated().sum():,}")

    print("\nFirst 3 Rows:")
    print(df.head(3))