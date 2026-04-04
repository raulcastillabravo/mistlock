from redis_client import RedisClient

def main():
    redis = RedisClient()
    redis.connect()
    
    try:
        print("\n--- Setting user data with HSET ---")
        redis.client.hset("user:1001", "name", "John Doe")
        redis.client.hset("user:1001", "email", "john@example.com")
        redis.client.hset("user:1001", "age", "30")
        
        print("\n--- Retrieving specific fields with HGET ---")
        name = redis.client.hget("user:1001", "name")
        email = redis.client.hget("user:1001", "email")
        
        print(f"\nUser 1001 details:")
        print(f"  Name: {name}")
        print(f"  Email: {email}")
        
        print("\n✓ Done! You can now see the data in Redis Insight.")
        
    except Exception as e:
        print(f"\n✗ Error occurred: {e}")
    finally:
        redis.close()

if __name__ == "__main__":
    main()