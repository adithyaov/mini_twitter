import web
import model

### Url mappings

urls = (
    '/', 'Index',
    '/seed', 'Seed',
    '/feed', 'Feed',
    '/me', 'Me',
    '/following', 'Following',
    '/users', 'User',
    '/session/(.*)', 'Session'
)


t_globals = {
    'datestr': web.datestr
}
render = web.template.render('templates', globals=t_globals)

class Seed:
    def GET(self):
        model.seed()

class Feed:
    def GET(self):
        r = model.get_tweets(1)
        return render.feed(r[0], r[1])

    def POST(self):
        post_data = web.input(_method='post')
        model.new_tweet(1, post_data['title'], post_data['content'])
        raise web.redirect('/feed')

class Me:
    def GET(self):
        me = model.get_me(1)
        return render.me(me[0], me[1])

class User:
    def GET(self, query):
        search_query = ""
        if query != None:
            search_query = query
        r = model.user_search(search_query)
        return render.users(r[0], r[1])

class Following:
    def GET(self):
        r = model.get_following(1)
        return render.following(r[0], r[1])



app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
