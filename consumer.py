import pika
import psycopg
import json
import os
from rabbitmq import consume_messages

# Environment variables for RabbitMQ and PostgreSQL connection
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "db")
DB_USERNAME = os.getenv("DB_USERNAME", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "my-secret-pw")

# PostgreSQL connection setup
def get_postgres_connection():
    conn = psycopg.connect(
        dbname=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST
    )
    return conn


# Function to check if a food exists by ISBN
def food_exists(name):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM foods WHERE name = %s", (name,))
            return cursor.fetchone() is not None
    finally:
        conn.close()


# Function to add a food to the database
def add_food_to_db(food_data):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO foods (name, restaurant, price, calories, category) VALUES (%s, %s, %s, %s, %s)",
                (
                    food_data["name"],
                    food_data["restaurant"],
                    food_data["price"],
                    food_data["calories"],
                    food_data["category"],
                ),
            )
            conn.commit()
    finally:
        conn.close()


# Callback function that will be triggered when a message is received from RabbitMQ
def callback(ch, method, properties, body):
    print("Received a new food message")

    food_data = json.loads(body)
    if not food_exists(food_data["name"]):
        print(
            f"Food with name {food_data['name']} does not exist, adding to the database."
        )
        add_food_to_db(food_data)
    else:
        print(f"Food with name {food_data['name']} already exists, skipping insertion.")

    # Acknowledge the message to RabbitMQ (message has been processed)
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Set up RabbitMQ connection and channel
def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    consume_messages(channel, queue_name="food_queue", callback=callback)


if __name__ == "__main__":
    start_consuming()
