from models import Base, Product
from db import get_engine, get_session
from datetime import datetime


def create_tables():
    engine = get_engine()
    Base.metadata.create_all(engine)


def insert_sample_data():
    session = get_session()

    try:
        # (name, category, price, quantity_sold, revenue, sale_date)
        products_data = [
            # Electronics
            ("Laptop Dell XPS 15", "Electronics", 1299.99, 52, 67599.48, datetime(2024, 10, 15)),
            ("iPhone 15 Pro", "Electronics", 999.99, 135, 134998.65, datetime(2024, 9, 22)),
            ("Samsung 4K TV 55\"", "Electronics", 699.99, 29, 20299.71, datetime(2024, 11, 3)),
            ("Sony Headphones WH-1000XM5", "Electronics", 349.99, 91, 31849.09, datetime(2024, 10, 8)),
            ("Apple Watch Series 9", "Electronics", 429.99, 105, 45148.95, datetime(2024, 9, 17)),
            
            # Clothing
            ("Nike Air Max Sneakers", "Clothing", 129.99, 168, 21838.32, datetime(2024, 10, 25)),
            ("Levi's 501 Jeans", "Clothing", 79.99, 215, 17197.85, datetime(2024, 9, 30)),
            ("Adidas Running Jacket", "Clothing", 89.99, 94, 8459.06, datetime(2024, 11, 12)),
            ("H&M Cotton T-Shirt", "Clothing", 19.99, 438, 8755.62, datetime(2024, 10, 2)),
            ("Zara Winter Coat", "Clothing", 159.99, 71, 11359.29, datetime(2024, 11, 18)),
            
            # Home & Kitchen
            ("KitchenAid Stand Mixer", "Home & Kitchen", 449.99, 45, 20249.55, datetime(2024, 9, 28)),
            ("Nespresso Coffee Machine", "Home & Kitchen", 199.99, 103, 20598.97, datetime(2024, 10, 14)),
            ("Dyson Vacuum Cleaner", "Home & Kitchen", 549.99, 53, 29149.47, datetime(2024, 11, 5)),
            ("Air Fryer 5L", "Home & Kitchen", 119.99, 147, 17638.53, datetime(2024, 9, 11)),
            ("Le Creuset Dutch Oven", "Home & Kitchen", 299.99, 58, 17399.42, datetime(2024, 10, 20)),
            
            # Books
            ("The Great Gatsby", "Books", 14.99, 298, 4467.02, datetime(2024, 9, 8)),
            ("1984 by George Orwell", "Books", 16.99, 325, 5521.75, datetime(2024, 10, 17)),
            ("Harry Potter Collection", "Books", 89.99, 156, 14038.44, datetime(2024, 11, 9)),
            ("The Lean Startup", "Books", 24.99, 210, 5247.90, datetime(2024, 9, 25)),
            ("Atomic Habits", "Books", 19.99, 279, 5577.21, datetime(2024, 10, 29)),
            
            # Sports & Outdoors
            ("Yoga Mat Premium", "Sports & Outdoors", 39.99, 189, 7558.11, datetime(2024, 9, 19)),
            ("Dumbbells Set 20kg", "Sports & Outdoors", 79.99, 102, 8158.98, datetime(2024, 10, 6)),
            ("Mountain Bike 27.5\"", "Sports & Outdoors", 599.99, 48, 28799.52, datetime(2024, 11, 15)),
            ("Camping Tent 4-Person", "Sports & Outdoors", 199.99, 74, 14799.26, datetime(2024, 9, 13)),
            ("Running Shoes Asics", "Sports & Outdoors", 119.99, 155, 18598.45, datetime(2024, 10, 22)),
        ]

        products = [
            Product(
                name=name,
                category=category,
                price=price,
                quantity_sold=quantity_sold,
                revenue=revenue,
                sale_date=sale_date
            )
            for name, category, price, quantity_sold, revenue, sale_date in products_data
        ]

        session.add_all(products)
        session.commit()
        print(f'Inserted {len(products)} products into the database')

    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    create_tables()
    insert_sample_data()
