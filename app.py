import json
import db

from flask import Flask, request

DB = db.DatabaseDrive()

app = Flask(__name__)


def success_response(data, code=200):
    return json.dumps({'success': True, 'data': data}), code


def failure_response(message, code=404):
    return json.dumps({'success': False, 'error': message}), code


@app.route("/")
@app.route("/tasks/")
def get_tasks():
    return success_response(DB.get_all_tasks())


@app.route("/tasks/", methods=["POST"])
def create_task():
    body = json.loads(request.data)
    description = body.get('description')
    task_id = DB.insert_task_table(description, False)
    task = DB.get_task_by_id(task_id)
    if task is not None:
        return success_response(task, 201)
    return failure_response("Something went wrong while creating task!")


@app.route("/tasks/<int:task_id>/")
def get_task(task_id):
    task = DB.get_task_by_id(task_id)
    if task is not None:
        return success_response(task)
    return failure_response("task not found!")


@app.route("/tasks/<int:task_id>/", methods=["POST"])
def update_task(task_id):
    body = json.loads(request.data)
    description = body.get('description')
    done = bool(body.get('done'))
    DB.update_task_by_id(task_id, description, done)

    task = DB.get_task_by_id(task_id)
    if task is not None:
        return success_response(task)
    return failure_response("Task not found!")


@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task(task_id):
    task = DB.get_task_by_id(task_id)
    if task is not None:
        DB.delect_task_by_id(task_id)
        return success_response(task)
    return failure_response('Task not found!')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
