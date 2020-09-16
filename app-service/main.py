import pika
import time
from random import randint
import os
import json
from customer import Customer

SLEEP_TIME = 10
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')


def rebase_customer(body):
    customer = json.loads(body.decode())
    new_customer = Customer.create(id=customer['id'], name=customer['name'])
    new_customer.save(force_insert=True)


def callback(ch, method, properties, body):
    retry_counter = 0
    if properties.headers:
        retry_counter = properties.headers.get('x-death')
        retry_counter = retry_counter[0]['count']

    print(f"[*] Recebido: [{retry_counter}] {body}")
    customer = json.loads(body.decode())
    if customer['name'] == 'Teste':
        if retry_counter < 5:
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            print('Rejeitada')
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        ch.basic_ack(delivery_tag=method.delivery_tag)


print("[*] Conectando no servidor  ... ")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='customer_analysis.q', on_message_callback=callback)
channel.start_consuming()
print("[*] Aguardando mensagens")
