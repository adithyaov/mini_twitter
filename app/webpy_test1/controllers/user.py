import web
from config import db_config

db = web.database(dbn=db_config['dbn'], db=db_config['db'])
render = web.template.render('views/user/')

class user:        
    def GET(self, id):
        constrains = dict(user_id=id)
        tweets = db.select('tweets', constrains, where="user_id = $user_id")
        return render.index(session, tweets)