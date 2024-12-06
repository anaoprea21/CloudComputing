import pika
import json
import os

# RabbitMQ connection settings
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

# Function to connect to RabbitMQ
def connect_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    return channel


# Function to declare the queue
def declare_queue(channel, queue_name="food_queue"):
    channel.queue_declare(queue=queue_name, durable=True)


# Function to send a message to a queue
def send_message(channel, queue_name, message):
    message_json = json.dumps(message)
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=message_json,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make the message persistent
        ),
    )
    print(f"Sent message to queue: {message}")


# Function to consume messages from a queue
def consume_messages(channel, queue_name="food_queue", callback=None):
    declare_queue(channel, queue_name)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print("Waiting for messages...")
    channel.start_consuming()
