from customer import Customer
from faker import Faker
import uuid


def create_data_fake():

    fake = Faker()

    Customer.create_table()

    id = uuid.uuid4()
    customer = Customer(id=id, name='Teste')
    customer.save(force_insert=True)
    print(customer.id, customer.name)

    for _ in range(10):
        id = uuid.uuid4()
        name = fake.name()
        customer = Customer(id=id, name=name)
        customer.save(force_insert=True)
        print(id, name)
