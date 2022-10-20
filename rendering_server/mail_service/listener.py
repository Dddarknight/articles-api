import aiohttp
import functools
import os
import pika
import requests
import smtplib
import ssl
import time
import threading
from dotenv import load_dotenv
from pika.exchange_type import ExchangeType


load_dotenv()

SMTP_SERVER = "smtp.gmail.com"

RABBIT_USER = os.getenv('RABBIT_USER')

RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD')

HOST = os.getenv('HOST')

RABBIT_PORT = os.getenv('RABBIT_PORT')

RABBIT_VIRTUAL_HOST = os.getenv('RABBIT_VIRTUAL_HOST')

EMAIL_PORT = os.getenv('EMAIL_PORT')

SENDER_EMAIL = os.getenv('SENDER_EMAIL')

SENDER_EMAIL_PASSWORD = os.getenv('SENDER_EMAIL_PASSWORD')


def ack_message(channel, delivery_tag):
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        pass


def do_work(channel, delivery_tag, body):
    email_function(body)
    cb = functools.partial(ack_message, channel, delivery_tag)
    channel.connection.add_callback_threadsafe(cb)


def on_message(channel, method_frame, header_frame, body, args):
    thrds = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(channel, delivery_tag, body))
    t.start()
    thrds.append(t)


def get_moderators_emails():
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(f'http://{HOST}:8080/moderators') as response:
    #         moderators = await response.json()
    response = requests.get(f'http://{HOST}:8080/moderators')
    moderators = response.json()
    emails = []
    for moderator in moderators:
        emails.append(moderator['email'])
    return emails


def email_function(message):
    emails = get_moderators_emails()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, EMAIL_PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
        for receiver_email in emails:
            server.sendmail(SENDER_EMAIL, receiver_email, message)
    time.sleep(5)
    return


# def callback(ch, method, properties, body):
#     email_function(body)


def listen_to_queue():
    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
    parameters = pika.ConnectionParameters(
        HOST, RABBIT_PORT, RABBIT_VIRTUAL_HOST, credentials, heartbeat=5)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.exchange_declare(
        exchange='registration',
        exchange_type=ExchangeType.direct)
    channel.queue_declare(queue='email_queue')
    channel.queue_bind(
        exchange='registration', queue='email_queue')
    channel.basic_qos(prefetch_count=1)

    # channel.basic_consume(
    #     'email_queue',
    #     callback,
    #     auto_ack=False)
    # try:
    #     for method, properties, body in channel.consume('email_queue', inactivity_timeout=5):
    #         if not body:
    #             break
    #         else:
    #             callback(channel, method, properties, body)
    # except KeyboardInterrupt:
    #     channel.stop_consuming()
    
    # channel.start_consuming()
    # channel.stop_consuming()
    
    threads = []
    on_message_callback = functools.partial(on_message, args=(threads))
    channel.basic_consume('email_queue', on_message_callback)
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    for thread in threads:
        thread.join()

    connection.close()