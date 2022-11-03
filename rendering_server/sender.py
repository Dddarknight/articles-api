import os
import pika
from dotenv import load_dotenv


load_dotenv()

RABBIT_USER = os.getenv('RABBIT_USER')

RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD')

HOST = os.getenv('HOST')

RABBIT_PORT = os.getenv('RABBIT_PORT')

RABBIT_HOST = os.getenv('RABBIT_HOST')


def send_to_queue(message, exchange, queue):
    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
    parameters = pika.ConnectionParameters(
        HOST, RABBIT_PORT, RABBIT_HOST, credentials,
        heartbeat=10, blocked_connection_timeout=5)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(
        queue=queue,
        arguments={"x-single-active-consumer": True})
    channel.exchange_declare(
        exchange=exchange)
    channel.queue_bind(
        exchange=exchange,
        queue=queue,
        routing_key=queue)
    channel.basic_publish(
        exchange=exchange,
        routing_key=queue,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2))
    connection.close()
