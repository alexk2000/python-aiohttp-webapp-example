from aiohttp import web


async def index(request):
    return web.Response(text='this is / of app2')

async def about(request):
    return web.Response(text='This is /about of app2')
