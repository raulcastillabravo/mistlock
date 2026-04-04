from models import User, get_connection

def insert_sample_data():
    """Insert sample users into MongoDB"""
    try:
        # Create sample users
        users_data = [
            {"name": "John Doe", "email": "john@example.com"},
            {"name": "Jane Smith", "email": "jane@example.com"},
            {"name": "Bob Johnson", "email": "bob@example.com"}
        ]
        
        created_users = []
        for user_data in users_data:
            user = User(**user_data)
            user.save()
            created_users.append(user)
        
        print(f"✓ Inserted {len(created_users)} users successfully")
        
        # Query and display inserted data
        all_users = User.objects.all()
        print("\nInserted users:")
        for user in all_users:
            print(f"  - {user}")
            
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    print("Connecting to MongoDB...")
    get_connection()
    print("✓ Connected successfully")
    
    print("\nInserting sample data...")
    insert_sample_data()
    
    print("\n✓ Done! You can now connect with MongoDB Compass to see the data.")