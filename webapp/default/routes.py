from .views import index, about


def setup_routes(app):
    app.router.add_get("/", index)
    app.router.add_get("/about/", about)
