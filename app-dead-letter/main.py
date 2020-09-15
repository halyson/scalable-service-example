import pika
import os
from customer import Customer
import json


SLEEP_TIME = 10
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')


def callback(ch, method, properties, body):
    print(f"[*] Recebido DLQ: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


print("[*] Conectando no servidor  ...")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

channel.exchange_declare(exchange='customer_analysis_dlx', exchange_type='direct', durable=True)
result = channel.queue_declare(queue='customer_analysis_dlq')
queue_name = result.method.queue
channel.queue_bind(exchange='customer_analysis_dlx',
                   routing_key='customer_analysis_dlq',  # x-dead-letter-routing-key
                   queue=queue_name)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)
channel.start_consuming()
print("[*] Aguardando mensagens")
