import pandas as pd
from minio_delta import MinioDelta


def main():
    client = MinioDelta()

    # Initial data
    sales_data = pd.DataFrame({
        'product_id': [1, 2, 3, 4, 5],
        'product_name': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'],
        'category': ['Electronics', 'Accessories', 'Accessories', 'Electronics', 'Accessories'],
        'price': [999.99, 25.50, 75.00, 349.99, 89.99],
        'quantity_sold': [15, 150, 85, 42, 68]
    })

    print("1. Writing partitioned Delta table by category...")
    client.write(sales_data, "sales_data", partition_by=["category"])

    # Read all data
    print("2. Reading all data:")
    all_data = client.read("sales_data")
    print(all_data)

    # Update only Electronics partition using predicate
    updated_electronics = pd.DataFrame({
        'product_id': [1, 4, 6],
        'product_name': ['Gaming Laptop', 'UltraWide Monitor', 'Webcam'],
        'category': ['Electronics', 'Electronics', 'Electronics'],
        'price': [1499.99, 499.99, 129.99],
        'quantity_sold': [25, 60, 35]
    })

    print("3. Overwriting only Electronics partition using predicate:")
    print(updated_electronics)
    client.write(
        updated_electronics, 
        "sales_data", 
        mode="overwrite",
        predicate="category = 'Electronics'"
    )

    # Read all data after update
    print("4. Reading all data after Electronics update:")
    final_data = client.read("sales_data")
    print(final_data)

    print(f"\nTotal products: {len(final_data)}")
    print(f"Electronics products: {len(final_data[final_data['category'] == 'Electronics'])}")
    print(f"Accessories products: {len(final_data[final_data['category'] == 'Accessories'])}")


if __name__ == "__main__":
    main()
