import web
web.config.debug = False

urls = (
    "/count", "count",
    "/reset", "reset"
)

app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={})

def auth_user(user):
    session.logged_in = True
    session.user_id = user.id
    session.username = user.username

def get_current_user():
    if session.logged_in:
        return User.get(User.id == session.user_id)

def login_required():
    if not session.logged_in:
        raise web.redirect('/login')

def get_object_or_throw(model, *expressions):
    try:
        return model.get(*expressions)
    except:
        raise web.redirect('/not_found')

def is_following(from_user, to_user):
    return from_user.is_following(to_user)

class Timeline:
    def GET(self):
        login_required()
        user = get_current_user()
        tweets = Tweet.select().where(Tweet.user << user.following())
        return render.timeline(tweets)

class Register:
    def POST(self):
        try:
            post_data = web.input(_method='post')
            with database.transaction():
                user = User.create(
                    username=post_data['username'],
                    password=post_data['password'],
                    email=post_data['email'],
                    join_date=datetime.datetime.now())

            auth_user(user)
            raise web.redirect('/timeline')
        except:
            raise web.redirect('/error')





if __name__ == "__main__":
    app.run()