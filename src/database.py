from peewee import *
import datetime
import os

if os.environ.get('MYSQL_HOST'):
    HOST = os.environ.get('MYSQL_HOST')
else:
    HOST = '127.0.0.1'


db = MySQLDatabase('steamitems', user='root',
                   password='mypassword;', port=3306, host=HOST)


class BaseModel(Model):
    class Meta:
        database = db


class App(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()


class Item(BaseModel):
    app = ForeignKeyField(App, to_field="id")
    name = CharField()
    tag = CharField()

    class Meta:
        indexes = (
            (("app", "tag"), True),
        )


class Skin(BaseModel):
    item = ForeignKeyField(Item)
    name = CharField()
    # TODO remove image size from url
    thumbnail = CharField()
    # TODO remove image size from url
    image = CharField(null=True)

    class Meta:
        indexes = (
            (("item", "name"), True),
        )


class Price(BaseModel):
    id = PrimaryKeyField()
    skin = ForeignKeyField(Skin)
    measured = DateTimeField(default=datetime.datetime.now)
    value = FloatField()
    currency = CharField()


def connect():
    db.connect()
    db.create_tables([App, Item, Skin, Price])
    return db
