import web
from model import *
web.config.debug = False

urls = (
    "/", "Home",
    "/home", "Home",
    "/login", "Login",
    "/logout", "Logout",
    "/following", "Following",
    "/followers", "Followers",
    "/users/(.*)", "Users",
    "/relation/(.+)/(.+)", "Relation"
)

app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'logged_in': False})

try:
    create_tables()
except:
    print 'Already created tables! :-)'

t_globals = {
    'datestr': web.datestr
}
render = web.template.render('templates', globals=t_globals)

def auth_user(user):
    session.logged_in = True
    session.user_id = user.id
    session.username = user.username

def get_current_user():
    if session.logged_in:
        return User.get(User.id == session.user_id)

def should_be_logged_in():
    if not session.logged_in:
        raise web.redirect('/login')

def should_be_logged_out():
    if session.logged_in:
        raise web.redirect('/timeline')

def get_object_or_throw(model, *expressions):
    try:
        return model.get(*expressions)
    except:
        return render.error('Not Found, 404!')

def is_following(from_user, to_user):
    return from_user.is_following(to_user)

class Home:
    def GET(self):
        return render.home()

class Timeline:
    def GET(self):
        should_be_logged_in()
        user = get_current_user()
        tweets = Tweet.select().where(Tweet.user << user.following())
        return render.timeline(tweets)

    def POST(self):
        should_be_logged_in()
        user = get_current_user()
        tweet = Tweet.create(
            user=user,
            content=request.form['content'],
            pub_date=datetime.datetime.now())
        raise web.redirect('/timeline')

class Register:
    def POST(self):
        should_be_logged_out()
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
            raise web.redirect('/register')

    def GET(self):
        should_be_logged_out()
        return render.register()


class Login:
    def POST(self):
        should_be_logged_out()
        try:
            post_data = web.input(_method='post')
            user = User.get(
                username=post_data['username'],
                password=post_data['password'])
        except:
            raise web.redirect('/login')
        else:
            auth_user(user)
            raise web.redirect('/timeline')

    def GET(self):
        should_be_logged_out()
        return render.login()


class Logout:
    def GET(self):
        should_be_logged_in()
        session.logged_in = False
        raise web.redirect('/home')

class Following:
    def GET(self):
        should_be_logged_in()
        user = get_current_user()
        return render.following(user.following())

class Followers:
    def GET(self):
        should_be_logged_in()
        user = get_current_user()
        return render.followers(user.followers())

class Users:
    def GET(self, username):
        should_be_logged_in()
        if username == None or username == '_':
            users = User.select()
            return render.users(users)
        else:
            user = get_object_or_throw(User, User.username == username)
            tweets = Tweet.select().where(user=user).order_by(('pub_date', 'desc'))
            return render.user_detail(user, tweets)

class Relation:
    def GET(self, username, action):
        should_be_logged_in()
        if action == 'follow':
            user = get_object_or_throw(User, User.username == username)
            try:
                with database.transaction():
                    Relationship.create(
                        from_user=get_current_user(),
                        to_user=user)
            except:
                pass
            raise web.redirect('/following')

        if action == 'unfollow':
            user = get_object_or_throw(User, User.username == username)
            Relationship.delete().where(
                (Relationship.from_user == get_current_user()) &
                (Relationship.to_user == user)
            ).execute()
            raise web.redirect('/following')


if __name__ == "__main__":
    app.run()