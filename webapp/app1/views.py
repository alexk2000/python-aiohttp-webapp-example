from aiohttp import web
from . import db
from ..utils import short_task
from aiojobs.aiohttp import setup, spawn

async def index(request):
    # await spawn(request, short_task())
    await request.app['scheduler'].spawn(short_task())
    return web.Response(text='This is / of app1')
    # return web.Response(text=request.app['data'])

async def about(request):
    print('about')
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.users.select())
        records = await cursor.fetchall()
        users = [dict(q) for q in records]
        # return {'questions': questions}

    return web.Response(text='This is /about of app1 {}'.format(users))
