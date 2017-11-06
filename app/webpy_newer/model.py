import datetime
from peewee import *

db = SqliteDatabase('main.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_date = DateTimeField()

    class Meta:
        order_by = ('username',)

    def following(self):
        return User.select().join(
            Relationship, on=Relationship.to_user,
        ).where(Relationship.from_user == self)

    def followers(self):
        return User.select().join(
            Relationship, on=Relationship.from_user,
        ).where(Relationship.to_user == self)

    def is_following(self, user):
        return Relationship.select().where(
            (Relationship.from_user == self) &
            (Relationship.to_user == user)
        ).count() > 0


class Relationship(BaseModel):
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')

    class Meta:
        indexes = ((('from_user', 'to_user'), True),)

class Tweet(BaseModel):
    user = ForeignKeyField(User)
    content = TextField()
    pub_date = DateTimeField()

    class Meta:
        order_by = ('-pub_date',)

def create_tables():
    db.connect()
    db.create_tables([User, Relationship, Tweet])