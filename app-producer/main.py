import pika
import os
from customer import Customer
import json

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')


connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))

channel = connection.channel()


channel.exchange_declare(exchange='customer_analysis_dl.x', exchange_type='direct', durable=True)
channel.exchange_declare(exchange='customer_analysis.x', exchange_type='direct', durable=True)

channel.queue_declare(queue='customer_analysis.q', durable=True,
                      arguments={
                          'x-dead-letter-exchange': 'customer_analysis_dl.x',
                          'x-dead-letter-routing-key': 'customer_analysis_dl.q',
                      }
                      )

channel.queue_declare(queue='customer_analysis_dl.q', durable=True,
                      arguments={
                          'x-message-ttl': 15000,
                          'x-dead-letter-exchange': 'customer_analysis.x',
                          'x-dead-letter-routing-key': 'customer_analysis.q',
                      }
                      )

channel.queue_bind(exchange='customer_analysis.x',
                   routing_key='customer_analysis.q',  # x-dead-letter-routing-key
                   queue='customer_analysis.q')

channel.queue_bind(exchange='customer_analysis_dl.x',
                   routing_key='customer_analysis_dl.q',  # x-dead-letter-routing-key
                   queue='customer_analysis_dl.q')


def rebase_customer(body):
    customer = json.loads(body.decode())
    new_customer = Customer.create(id=customer['id'], name=customer['name'])
    new_customer.save(force_insert=True)


for customer in Customer.select():
    customer_data = {
        'id': str(customer.id),
        'name': customer.name
    }
    customer_data = json.dumps(customer_data)
    print(f'Enviado - {customer_data}')
    channel.basic_publish(
        exchange='',
        routing_key='customer_analysis.q',
        body=customer_data,
        properties=pika.BasicProperties(delivery_mode=2))
    customer.delete_instance()

connection.close()
