import pika
import os
from dotenv import load_dotenv

load_dotenv()

class RabbitMQClient:
    
    def __init__(self, queue_name: str):
        self.host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.port = int(os.getenv('RABBITMQ_PORT', 5672))
        self.user = os.getenv('RABBITMQ_USER')
        self.password = os.getenv('RABBITMQ_PASSWORD')
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
    
    def connect(self):
        """Establish connection to RabbitMQ"""
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        return self.channel
    
    def publish(self, message: str):
        """Publish a message to the queue"""
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
    
    def start_consuming(self, callback):
        """Start listening for messages with a custom callback"""
        self.channel.basic_qos(prefetch_count=1)
        
        def wrapped_callback(ch, method, properties, body):
            callback(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=wrapped_callback
        )
        
        print(f"\n--- Listening for events on queue '{self.queue_name}' ---")
        print("✓ Waiting for messages. Press CTRL+C to exit\n")
        
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print("\n\n✓ Stopped listening")
            self.channel.stop_consuming()
        finally:
            self.close()
    
    def close(self):
        """Close RabbitMQ connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()