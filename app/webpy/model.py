import web

db = web.database(dbn='sqlite', db='main.sqlite')

def get_tweets(user_id):
    constrains = dict(user_id=user_id)
    return db.select('Tweets', where=web.db.sqlwhere(constrains), order='id DESC')

def user_search(query):
    if query.strip() == "":
        return db.select('Users')
    else:
        return db.select('Users')

def new_tweet(user_id, title, text):
    db.insert('Tweets', user_id=user_id, title=title, content=text)

def del_tweet(user_id, tweet_id):
    constrains = dict(user_id=user_id, id=tweet_id)
    db.delete('Tweets', where=web.db.sqlwhere(constrains), vars=locals())