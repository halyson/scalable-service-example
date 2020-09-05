from customer import Customer
from faker import Faker
import uuid

fake = Faker()

Customer.create_table()

for _ in range(100):
    id = uuid.uuid4()
    name = fake.name()
    customer = Customer(id=id, name=name)
    customer.save(force_insert=True)
    print(id, name)
