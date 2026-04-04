from rabbitmq_client import RabbitMQClient

def callback(body):
    """Callback function to process received messages"""
    message = body.decode('utf-8')
    print(f"✓ Received: {message}")

def main():
    queue_name = "user_events"
    
    rabbitmq = RabbitMQClient(queue_name)
    rabbitmq.connect()
    rabbitmq.start_consuming(callback)

if __name__ == "__main__":
    main()