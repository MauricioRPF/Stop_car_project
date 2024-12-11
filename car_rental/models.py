from peewee import *

db = PostgresqlDatabase('carrentaldb', user='mallzz', password='mallzz52', host='db', port=5432)

class User(Model):
    name = CharField()
    gender = CharField()
    cpf = CharField(unique=True)
    birth_date = DateField()
    email = CharField()
    phone_number = CharField()
    car_model = CharField()

    class Meta:
        database = db

# To create the tables, use:
db.connect()
db.create_tables([User])
