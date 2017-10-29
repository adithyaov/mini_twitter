import web
from routes import urls
from config import db_config
db = web.database(dbn=db_config['dbn'], db=db_config['db'])

# Only for testing
from helpers.init_tables import init_tables
print init_tables(db_config['db'])

app = web.application(urls, globals())

class hello:        
    def GET(self, name):
        if not name: 
            name = 'World'
        return 'Hello, ' + name + '!'

if __name__ == "__main__":
    app.run()
