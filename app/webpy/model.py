

from peewee import *

db = SqliteDatabase('main.db')

class User(Model):
    name = CharField()
    image = TextField()
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
    t1 = Tweet(user_id=1, title='Hello World', content='Sahely ki Jai!')
    t2 = Tweet(user_id=1, title='Hello World Again', content='Mrinal ki Jai!')
    u1 = User(name="varshith",image = "kjh", email="varshithpolu@polu.com")
    u2 = User(name="aditya",image = "kjh", email="adityas@polu.com")
    u3 = User(name="nishanth",image = "kjh", email="nishanth@polu.com")

    f1 = Following(user_id = 1,following_ids = "1,2")
    t1.save()
    t2.save()
    u1.save()
    u2.save()
    u3.save()
    f1.save()

def get_tweets(user_id):
    try:
        q = Tweet.select().where(Tweet.user_id == user_id)
        return (True, q)
    except Exception as e:
        return (False, e)

def get_me(user_id):
    try:
        q = User.select().where(User.id == user_id).get()
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


def get_following(user_id):
    try:
        q = Following.select().where(Following.user_id == user_id).get()
        following_ids = q.following_ids
        following_ids_list = following_ids.split(',')
        q2 = User.select().where(User.id in following_ids_list)
        return (True, q2)
    except Exception as e:
        return (False, e)