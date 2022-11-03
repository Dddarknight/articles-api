import os
import pika
import requests
import smtplib
import ssl
from dotenv import load_dotenv


load_dotenv()

SMTP_SERVER = "smtp.gmail.com"

RABBIT_USER = os.getenv('RABBIT_USER')

RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD')

HOST = os.getenv('HOST')

API_PORT = os.getenv('API_PORT')

URL_MODERATORS = f'http://{HOST}:{API_PORT}/moderators'

RABBIT_PORT = os.getenv('RABBIT_PORT')

RABBIT_HOST = os.getenv('RABBIT_HOST')

EMAIL_PORT = os.getenv('EMAIL_PORT')

SENDER_EMAIL = os.getenv('SENDER_EMAIL')

SENDER_EMAIL_PASSWORD = os.getenv('SENDER_EMAIL_PASSWORD')


class Listener:
    def get_moderators_emails(self):
        response = requests.get(URL_MODERATORS)
        moderators = response.json()
        emails = []
        for moderator in moderators:
            emails.append(moderator['email'])
        return emails

    def send_email(self, message):
        emails = self.get_moderators_emails()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
                SMTP_SERVER, EMAIL_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
            for receiver_email in emails:
                server.sendmail(SENDER_EMAIL, receiver_email, message)
        return

    def callback(self, ch, method, properties, message):
        self.send_email(message)

    def listen_to_queue(self, exchange, queue):
        credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
        parameters = pika.ConnectionParameters(
            HOST, RABBIT_PORT, RABBIT_HOST, credentials)
        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()
        channel.exchange_declare(
            exchange=exchange)
        channel.queue_declare(
            queue=queue,
            arguments={"x-single-active-consumer": True})
        channel.queue_bind(
            exchange=exchange,
            queue=queue,
            routing_key=queue)
        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(
            queue, on_message_callback=self.callback, auto_ack=True)

        channel.start_consuming()
