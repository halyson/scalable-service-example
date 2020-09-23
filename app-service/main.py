import pika
import time
from random import randint
import os
import json
import time
from customer_processed import CustomerProcessed

SLEEP_TIME = 10
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')


def process_customer(customer) -> bool:
    time.sleep(2)
    new_customer_processed = CustomerProcessed.create(id=customer['id'], name=customer['name'].upper())
    new_customer_processed.save()
    print('Customer Processado!')
    return True


def callback(ch, method, properties, body):
    retry_counter = 0
    if properties.headers:
        retry_counter = properties.headers.get('x-death')
        retry_counter = retry_counter[0]['count']

    print(f"[*] Recebido: [{retry_counter}] {body}")
    customer_data = json.loads(body.decode())
    if customer_data['name'] == 'Teste':
        if retry_counter < 5:
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            print('Rejeitado')
        else:
            print('Customer não processado e removido da fila...')
            ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        process_customer(customer_data)
        ch.basic_ack(delivery_tag=method.delivery_tag)


CustomerProcessed.create_table()

print("[*] Conectando no servidor  ... ")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='customer_analysis.q', on_message_callback=callback)
channel.start_consuming()
print("[*] Aguardando mensagens")
