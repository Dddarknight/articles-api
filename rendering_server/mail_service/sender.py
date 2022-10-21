import os
import pika
from dotenv import load_dotenv


load_dotenv()

RABBIT_USER = os.getenv('RABBIT_USER')

RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD')

HOST = os.getenv('HOST')

RABBIT_PORT = os.getenv('RABBIT_PORT')

RABBIT_VIRTUAL_HOST = os.getenv('RABBIT_VIRTUAL_HOST')

MESSAGE = "A user has registered"


def send_to_queue():
    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
    parameters = pika.ConnectionParameters(
        HOST, RABBIT_PORT, RABBIT_VIRTUAL_HOST, credentials,
        heartbeat=10, blocked_connection_timeout=5)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(
        queue='email_queue',
        arguments={"x-single-active-consumer": True},
        auto_delete=True)
    channel.exchange_declare(
        exchange='registration')
    channel.queue_bind(
        exchange='registration',
        queue='email_queue',
        routing_key='email_queue')
    channel.basic_publish(
        exchange='registration',
        routing_key='email_queue',
        body=MESSAGE,
        properties=pika.BasicProperties(
            delivery_mode=2))
    connection.close()
