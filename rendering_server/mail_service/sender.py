import os
import pika
from pika.exchange_type import ExchangeType
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
        HOST, RABBIT_PORT, RABBIT_VIRTUAL_HOST, credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(
        queue='email_queue')
    channel.exchange_declare(
        exchange='registration',
        exchange_type=ExchangeType.direct)
    channel.basic_publish(
        exchange='registration', routing_key='email_queue', body=MESSAGE)
    connection.close()
