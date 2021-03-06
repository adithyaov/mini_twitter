import web
import datetime
from model import *
web.config.debug = False

urls = (
    "/", "Login",
    "/home", "Login",
    "/login", "Login",
    "/logout", "Logout",
    "/following", "Following",
    "/followers", "Followers",
    "/users/(.*)", "Users",
    "/relation/(.+)/(.+)", "Relation",
    "/timeline", "Timeline",
    "/register", "Register",
    "/test/(.*)", "Test",
    "/*", "Login",
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
    if session.logged_in == False:
    	print "login"
        raise web.seeother('/login')

def should_be_logged_out():
    if session.logged_in == True:
        print "logout"
        raise web.seeother('/timeline')

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
        return render.timeline(session, tweets)

    def POST(self):
        should_be_logged_in()
        user = get_current_user()
        post_data = web.input(_method='post')
        with db.transaction():
            tweet = Tweet.create(
                user=user,
                content=post_data.content,
                pub_date=datetime.datetime.now())
        raise web.seeother('/timeline')

class Register:
    def POST(self):
        should_be_logged_out()
        echo = 0
        try:
            post_data = web.input(_method='post')
            with db.transaction():
                user = User.create(
                    username=post_data['username'],
                    password=post_data['password'],
                    email=post_data['email'],
                    join_date=datetime.datetime.now())

                Relationship.create(
                    from_user=user,
                    to_user=user)

                auth_user(user)

            echo = 1
        except Exception as e:
            print e
            echo = 0

        if echo == 1:
            raise web.seeother('/timeline')
        else:
            raise web.seeother('/register')

    def GET(self):
        should_be_logged_out()
        return render.register()


class Login:
    def POST(self):
        should_be_logged_out()
        echo = 0
        try:
            post_data = web.input(_method='post')
            user = User.get(
                username=post_data['username'],
                password=post_data['password'])
            auth_user(user)
            echo = 1
        except Exception as e:
            print e
            echo = 0
            
        if echo == 1:
            raise web.seeother('/timeline')
        else:
            raise web.seeother('/login')



    def GET(self):
        should_be_logged_out()
        return render.login()


class Logout:
    def GET(self):
        should_be_logged_in()
        session.logged_in = False
        session.user_id = -1
        session.username = ''
        raise web.seeother('/home')

class Following:
    def GET(self):
        should_be_logged_in()
        user = get_current_user()
        return render.following(session, user.following())

class Followers:
    def GET(self):
        should_be_logged_in()
        user = get_current_user()
        return render.followers(session, user.followers())

class Users:
    def GET(self, username):
        should_be_logged_in()
        if username == None or username == '_' or username == '':
            user = get_current_user()
            following_users = get_current_user().following()
            following_usernames = []
            for x in following_users:
                following_usernames.append(x.username)
            users = User.select().where(User.username.not_in(following_usernames))
            return render.users(session,users)
        else:
            user = get_object_or_throw(User, User.username == username)
            tweets = Tweet.select().where(Tweet.user==user)
            is_following = get_current_user().is_following(user)
            return render.user_detail(session, user, tweets, is_following)

class Relation:
    def GET(self, username, action):
        should_be_logged_in()
        if action == 'follow':
            user = get_object_or_throw(User, User.username == username)
            try:
                with db.transaction():
                    Relationship.create(
                        from_user=get_current_user(),
                        to_user=user)
            except:
                pass
            raise web.seeother('/following')

        if action == 'unfollow':
            user = get_object_or_throw(User, User.username == username)
            if user.username == session.username:
                raise web.seeother('/following')
            Relationship.delete().where(
                (Relationship.from_user == get_current_user()) &
                (Relationship.to_user == user)
            ).execute()
            raise web.seeother('/following')

class Test:
	def GET(self, message):
	    return render.error(message)

if __name__ == "__main__":
    app.run()
