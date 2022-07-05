from aiohttp import web
from webapp.app1 import db
import aiohttp_jinja2

@aiohttp_jinja2.template('index.html')
async def index(request):
    request.app['counter'] += 1
    return {'counter': request.app['counter']}

async def about(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.users.select())
        records = await cursor.fetchall()
        users = [dict(q) for q in records]

    return web.Response(text='This is /about of main {}'.format(users))