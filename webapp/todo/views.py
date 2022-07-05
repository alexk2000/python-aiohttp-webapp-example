from aiohttp import web
from . import db
import aiohttp_jinja2


class RecordNotFound(Exception):
    """Requested record in database was not found"""

class RowValidationError(Exception):
    """Requested record in database was not found"""

@aiohttp_jinja2.template('ajaxTimer.html')
async def index(request):
    return
    # return web.Response(text='This is / of todo app')

@aiohttp_jinja2.template('jqgrid.html')
async def jqgrid(request):
    return

class ApiTable(web.View):
    """Implements RESTAPI interface for the sql table

      todo: at the moment only one column primary key (integer) supported (most used case)
    """

    def __init__(self, app, prefix, table, col=None, headers=None):
        """This function does something.

        :param name: The name to use.
        :type name: str.
        :param state: Current state to be in.
        :type state: bool.
        :returns:  int -- the return code.
        :raises: AttributeError, KeyError

        """

        # critical checks
        pkeys = list(table.primary_key)
        if len(pkeys) != 1:
            print('error, no primary key or primary key consists of two or more columns')
            return False

        self.pkey_name = pkeys[0].name
        self.table = table
        if headers:
            self.headers = headers
        else:
            # default headers
            self.headers = {'Access-Control-Allow-Origin': '*'}

        self.url_names = {}
        for key in ['get_all', 'add_one', 'get_one_by_pkey', 'update_one', 'delete_one']:
            self.url_names[key] = '{}_{}'.format(self.table.name, key)

        # setup routes
        app.router.add_get("{}/{}".format(prefix, table), self.get_all, name=self.url_names['get_all'])
        app.router.add_post("{}/{}".format(prefix, table), self.add_one, name=self.url_names['add_one'])
        app.router.add_get("{}/{}/{{pkey}}".format(prefix, table), self.get_one_by_pkey,
                           name=self.url_names['get_one_by_pkey'])
        app.router.add_put("{}/{}/{{pkey}}".format(prefix, table), self.update_one, name=self.url_names['update_one'])
        app.router.add_delete("{}/{}/{{pkey}}".format(prefix, table), self.delete_one, name=self.url_names['delete_one'])

        # all column without primary key
        self.col_all = [c.name for c in table.c]
        if self.pkey_name in self.col_all:
            self.col_all.remove(self.pkey_name)
        # mandatory fields for add/update
        self.col_mandatory = self.col_all
        if col:
            self.col_mandatory = col

    # get all records
    async def get_all(self, request):
        async with request.app['db'].acquire() as conn:
            cursor = await conn.execute(self.table.select())
            records = await cursor.fetchall()
            records_list = []
            for record in records:
                temp = dict(record)
                temp['uri'] = '{}://{}{}'.format(
                    request.scheme,
                    request.host,
                    str(request.app.router[self.url_names['get_one_by_pkey']].url_for(pkey=str(temp[self.pkey_name])))
                )
                records_list.append(temp)
            return web.json_response({self.table.name: records_list},
                                     headers=self.headers)

    # general function, returns record in table by pkey
    async def get_record(self, conn, pkey):
        """
        :param app: aiohttp app instance
        :param prefix: restapi url
        :param table: sqlalchemy table definition
        :param col: mandatory columns for api add requests
        """
        result = await conn.execute(
            self.table.select().where(self.table.c[self.pkey_name] == pkey))
        record = await result.first()
        if not record:
            msg = "Record in table {} with id {} does not exists"
            raise RecordNotFound(msg.format(self.table, pkey))
        return record

    async def get_one_by_pkey(self, request):
        """ Hello how are you """
        async with request.app['db'].acquire() as conn:
            try:
                record = await self.get_record(conn, request.match_info['pkey'])
            except RecordNotFound as e:
                return web.json_response({'error': str(e)}, status=404)
            record_json = dict(record)
            print(record_json)
        return web.json_response({self.table.name: record_json},
                                 headers=self.headers)

    def validation(self, row):
        # data validation
        # check if all mandatory column presented in post data
        for col in self.col_mandatory:
            if col not in row:
                raise RowValidationError('field \'{}\' missing'.format(col))

        # check if no unknown data in post (no such column in table)
        for col in row.keys():
            if col not in self.col_all:
                raise RowValidationError('field \'{}\' in request is unknown'.format(col))

        return True

    async def add_one(self, request):
        if request.content_type == 'application/x-www-form-urlencoded':
            row_post1 = await request.post()
            row_post = dict(row_post1)
            del row_post['oper']
            del row_post['id']
        elif request.content_type == 'application/json':
            row_post = await request.json()

        try:
            status = self.validation(row_post)
        except RowValidationError as e:
            return web.json_response({
                'error': 'data validation error, {}'.format(str(e))
            }, status=400)

        async with request.app['db'].acquire() as conn:
            cursor = await conn.execute(self.table.insert().values(**row_post))
            records = await cursor.fetchall()
        return web.json_response({'status': 'added, id {}'.format(records[0][0])},
                                headers=self.headers, status=201)

    async def update_one(self, request):
        if request.content_type == 'application/x-www-form-urlencoded':
            record_request1 = await request.post()
            record_request = dict(record_request1)
            del record_request['oper']
            del record_request['id']

        elif request.content_type == 'application/json':
            record_request = await request.json()

        async with request.app['db'].acquire() as conn:
            pkey = request.match_info['pkey']
            try:
                record = await self.get_record(conn, pkey)
            except RecordNotFound as e:
                return web.json_response({'error': str(e)}, status=404)
            record_db = dict(record)

            record_updated = {}
            for col, val in record_db.items():
                record_updated[col] = record_request.get(col, record_db[col])
            try:
                await conn.execute(self.table.update().where(self.table.c[self.pkey_name] == pkey).values(**record_updated))
            except TypeError as e:
                return web.json_response({'error': str(e)}, status=400)
        return web.json_response({self.table.name: record_updated}, headers=self.headers)

    async def delete_one(self, request):
        async with request.app['db'].acquire() as conn:
            await conn.execute(self.table.delete().where(db.tasks.c.id.in_(request.match_info['pkey'].split(','))))

        return web.json_response({'status': 'deleted'}, headers=self.headers)
