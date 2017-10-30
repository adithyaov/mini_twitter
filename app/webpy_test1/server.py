import web
from routes import urls
from config import db_config
from controllers.hello import hello
from controllers.user import user

# Only for testing
from helpers.init_tables import init_tables
print init_tables(db_config['db'])

db = web.database(dbn=db_config['dbn'], db=db_config['db'])

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
