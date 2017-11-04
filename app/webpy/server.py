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

class Me:
    def GET(self):
        test_data = {
            "name": "Varshith Polu",
            "email": "111501020@samil.iitpkd.ac.in",
            "image": "https://images.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.t7pp36obNYiHr92yA_ko8QEsDH%26pid%3D15.1&f=1"
        }
        return render.me(True, test_data)



app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
