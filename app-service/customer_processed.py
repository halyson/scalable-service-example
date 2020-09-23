import peewee

db = peewee.SqliteDatabase('data/customers_database.db')


class CustomerProcessed(peewee.Model):
    id = peewee.UUIDField(primary_key=True)
    name = peewee.CharField()

    class Meta:
        database = db
