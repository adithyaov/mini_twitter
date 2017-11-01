# import web

# db = web.database(dbn='sqlite', db='main.sqlite')

# def get_tweets(user_id):
#     constrains = dict(user_id=user_id)
#     return db.select('Tweets', where=web.db.sqlwhere(constrains), order='id DESC')

# def user_search(query):
#     if query.strip() == "":
#         return db.select('Users')
#     else:
#         return db.select('Users')

# def new_tweet(user_id, title, text):
#     db.insert('Tweets', user_id=user_id, title=title, content=text)

# def del_tweet(user_id, tweet_id):
#     constrains = dict(user_id=user_id, id=tweet_id)
#     db.delete('Tweets', where=web.db.sqlwhere(constrains), vars=locals())

from peewee import *

db = SqliteDatabase('main.db')

class User(Model):
    name = CharField()
    password = CharField()
    email = CharField(unique=True)
    class Meta:
        database = db

class Tweet(Model):
    title = CharField()
    content = CharField()
    user_id = IntegerField()
    class Meta:
        database = db

class Following(Model):
    user_id = IntegerField()
    following_ids = TextField()
    class Meta:
        database = db
try:
    db.create_tables([User, Tweet, Following])
except:
    pass

def get_tweets(user_id):
    return Tweet.select().where(Tweet.user_id == user_id)