import pika
import time
from random import randint
import os

SLEEP_TIME = 10
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')


def callback(ch, method, properties, body):
    print(f"[*] Recebido: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


print("[*] Conectando no servidor  ...")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='customer_analysis', on_message_callback=callback)
channel.start_consuming()
print("[*] Aguardando mensagens")
