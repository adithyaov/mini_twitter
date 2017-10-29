import web

render = web.template.render('views/hello/')

class hello:        
    def GET(self, name):
        return render.index(name)