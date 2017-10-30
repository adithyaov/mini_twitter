import web
from config import db_config

db = web.database(dbn=db_config['dbn'], db=db_config['db'])
render = web.template.render('views/tweets/')

class tweets:        
    def GET(self):
        constrains = dict(user_id=1)
        tweets = db.select('tweets', constrains, where="user_id = $user_id")
        return render.index(session, tweets)