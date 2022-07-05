from .views import index, about

def setup_routes(app, prefix='/'):
    app.router.add_get("{}".format(prefix), index)
    app.router.add_get("{}about/".format(prefix), about)