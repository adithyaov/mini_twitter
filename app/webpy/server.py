import web
import model

### Url mappings

urls = (
    '/', 'Index',
    '/seed', 'Seed',
    '/feed', 'Feed',
    '/me', 'Me',
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



app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()