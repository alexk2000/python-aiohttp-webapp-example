from .views import index, jqgrid, ApiTable
from . import db

def setup_routes(app, prefix='/'):
    app.router.add_get("{}".format(prefix), index)
    app.router.add_get("{}jqgrid/".format(prefix), jqgrid)

    # # api implementation by function handlers
    # app.router.add_get("{}api/v1.0/tasks".format(prefix), api_v11_tasks, name='api_v11_tasks')
    # app.router.add_get("{}api/v1.0/tasks/{{task_id}}".format(prefix), api_v11_get_task)
    # app.router.add_post("{}api/v1.0/tasks".format(prefix), api_v11_add_task)
    # app.router.add_put("{}api/v1.0/tasks/{{task_id}}".format(prefix), api_v11_update_task)
    # app.router.add_delete("{}api/v1.0/tasks/{{task_id}}".format(prefix), api_v11_delete_task)
    # app.router.add_get("{}api/v1.0/test".format(prefix), api_v11_test)
    # # --

    # api implementation for any tables using class based views
    # col is mandatory fields for add/update api requests
    ApiTable(app, "{}api/v1.0".format(prefix), db.tasks, col=['title', 'description'])
    ApiTable(app, "{}api/v1.0".format(prefix), db.users, col=['name', 'password'])

