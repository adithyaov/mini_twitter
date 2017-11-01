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

def seed():
    Tweet(user_id=1, title='Hello World', content='Sahely ki Jai!')
    Tweet(user_id=1, title='Hello World Again', content='Mrinal ki Jai!')

def get_tweets(user_id):
    try:
        q = Tweet.select().where(Tweet.user_id == user_id)
        return (True, q)
    except Exception as e:
        return (False, e)

def user_search(query):
    try:
        if query.strip() == "":
            q = User.select()
            return (True, q)
        else:
            q = User.select().where(User.name == query)
            return (True, q)
    except Exception as e:
        return (False, e)

def new_tweet(user_id, title, content):
    try:
        t = Tweet(user_id=user_id, title=title, content=content)
        t.save()
        return (True, t)
    except Exception as e:
        return (False, e)

def del_tweet(user_id, tweet_id):
    try:
        q = Tweet.delete().where(Tweet.id == tweet_id, Tweet.user_id == user_id)
        q.execute()
        return (True)
    except Exception as e:
        return (False, e)