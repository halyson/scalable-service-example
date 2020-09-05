import pika
import os
from customer import Customer
import json

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue='customer_analysis', durable=True)


for customer in Customer.select():
    customer_data = {
        'id': str(customer.id),
        'name': customer.name
    }
    customer_data = json.dumps(customer_data)
    print(f'Enviado - {customer_data}')
    channel.basic_publish(
        exchange='',
        routing_key='customer_analysis',
        body=customer_data,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    customer.delete_instance()

connection.close()
