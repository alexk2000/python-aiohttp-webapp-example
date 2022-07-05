import aiofiles
import asyncio

# starting on app startup
async def bg_task1(app):
    try:
        async with aiofiles.open('/tmp/filename', mode='a') as f:
            while True:
                await asyncio.sleep(5)
                print('task_forever 5 seconds')
                await f.write('task_forever 5 seconds\n')
                await f.flush()
    except asyncio.CancelledError:
        pass

# starting in handler
async def short_task():
    try:
        async with aiofiles.open('/tmp/short_task', mode='a') as f:
            await asyncio.sleep(15)
            print('short task 15 seconds')
            await f.write('short task 15 seconds\n')
            await f.flush()
    except asyncio.CancelledError:
        pass

async def bg_task1_start(app):
    app['bg_task1'] = app.loop.create_task(bg_task1(app))

async def bg_task1_cleanup(app):
    app['bg_task1'].cancel()
    await app['bg_task1']