# import aiopg
from aiopg.sa import create_engine
# import sqlalchemy as sa
from aiohttp import web
import webapp.default.routes
import webapp.app1.routes
import webapp.app2.routes
import webapp.todo.routes
from webapp.middlewares import setup_middlewares
import aiohttp_jinja2
import jinja2
import pathlib
from webapp.utils import bg_task1_start, bg_task1_cleanup
import aiojobs
import uvloop
import asyncio

PROJECT_ROOT = pathlib.Path(__file__).parent
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def init_pg(app):
    conf = app['config']['postgres']
    # engine = await aiopg.sa.create_engine(
    engine = await create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        loop=app.loop)
    app['db'] = engine

async def init_aiojobs(app):
    app['scheduler'] = await aiojobs.create_scheduler()

async def close_aiojobs(app):
    await app['scheduler'].close()

async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()

def main(config=None):
    # main app
    app_main = web.Application()
    # postgres init
    app_main.on_startup.append(init_pg)
    # example of background task
    app_main.on_startup.append(bg_task1_start)
    # shot task used in webapp.app1.views.index()
    app_main.on_startup.append(init_aiojobs)

    app_main.on_cleanup.append(close_pg)
    app_main.on_cleanup.append(bg_task1_cleanup)
    app_main.on_cleanup.append(close_aiojobs)

    # config from config.yml
    app_main['config'] = config
    # example of global variable
    app_main['counter'] = 0

    # add handling static
    app_main.router.add_static('/static/',
                               path=str(PROJECT_ROOT / 'static'),
                               name='static')
    # main app routes
    default.routes.setup_routes(app_main)
    # app1 routes
    app1.routes.setup_routes(app_main, prefix='/app1/')
    # app2 routes
    app2.routes.setup_routes(app_main, prefix='/app2/')
    # todo routes
    todo.routes.setup_routes(app_main, prefix='/todo/')

    aiohttp_jinja2.setup(app_main, loader=jinja2.PackageLoader('webapp', 'templates'))
    
    setup_middlewares(app_main)

    return web.run_app(app_main, host=config.get('host', '127.0.0.1'), port=config.get('port', 8080))
