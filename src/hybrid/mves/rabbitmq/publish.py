from rabbitmq_client import RabbitMQClient
import random

def main():
    queue_name = "user_events"
    
    rabbitmq = RabbitMQClient(queue_name)
    rabbitmq.connect()
    
    try:
        # List of possible events
        events = [
            "User registered: john@example.com",
            "User logged in: jane@example.com",
            "User updated profile: bob@example.com"
        ]
        
        # Select a random event
        event = random.choice(events)
        
        print("\n--- Publishing event to RabbitMQ ---")
        rabbitmq.publish(event)
        print(f"✓ Published: {event}")
        print(f"\n✓ Done! Event published to queue '{queue_name}'")
        print("✓ You can run listen.py to consume this event")
        
    except Exception as e:
        print(f"\n✗ Error occurred: {e}")
    finally:
        rabbitmq.close()

if __name__ == "__main__":
    main()