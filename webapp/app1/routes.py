from .views import index, about
from aiohttp import web


def setup_routes(app, prefix='/'):
    # about_url = "{}about/".format(prefix)
    # print(about_url)
    app.add_routes([
        web.get("{}".format(prefix), index, name='index'),
        web.get("{}about/".format(prefix), about, name='about')
    ])
    # app.router.add_get("/", index, name='index')
    # app.router.add_get("/about/", about, name='about')