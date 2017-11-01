import web
import model

### Url mappings

urls = (
    '/', 'Index',
    '/feed', 'Feed',
    '/me', 'Me',
    '/users', 'User',
    '/session/(.*)', 'Session'
)


t_globals = {
    'datestr': web.datestr
}
render = web.template.render('templates', globals=t_globals)


class Feed:
    def GET(self):
        tweets = model.get_tweets(1)
        return render.feed(tweets)



app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()