import sqlite3 as lite
import os

def touch(path, mode='w'):
    with open(path, mode):
        os.utime(path, None)

def init_tables(path, mode='w'):
    try:
        touch(path, mode)
        con = lite.connect(path)
        with con:
            cur = con.cursor()    
            cur.execute("CREATE TABLE Users(id INT, name TEXT, password TEXT, email TEXT)")
            cur.execute("CREATE TABLE Tweets(id INT, title TEXT, body TEXT, user_id INT)")
            cur.execute("CREATE TABLE Following(id INT, user_id INT, following_ids TEXT)")
        return {
            "status": True
        }
    except Exception as e:
        return {
            "status": False,
            "error": e
        }