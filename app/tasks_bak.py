from flask import Blueprint, jsonify, request, Response
from flask_expects_json import expects_json

task_blue = Blueprint('tasks', __name__)

schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'id': {'type': 'integer'},
        'status': {'type': 'integer'}  # can't check boolean using 01, need True False
    },
    'required': ['name']
}

tasks_data_id = 1  # task start id
tasks_data = dict()  # task DB


@task_blue.route('/tasks', methods=['GET'])
def get_list_tasks():
    task_list = [{"id": i, "name": "name", "status": 0} for i in range(1, 2)]
    response = jsonify({'result': task_list})
    return response


@task_blue.route('/task', methods=['POST'])
@expects_json(schema)
def create_task():
    global tasks_data_id
    global tasks_data

    request_body = request.get_json(force=True)
    task_name = request_body.get('name')
    tasks_data[tasks_data_id] = {'result': {'name': task_name, 'status': 0, 'id': tasks_data_id}}

    response = jsonify(tasks_data[tasks_data_id])
    response.status_code = 201
    tasks_data_id += 1

    return response


@task_blue.route('/task/<int:num>', methods=['PUT'])
@expects_json(schema)
def update_task(num):
    global tasks_data_id
    global tasks_data

    request_body = request.get_json(force=True)
    task_id = request_body.get('id')
    task_status = request_body.get('status')
    task_name = request_body.get('name')
    if task_id not in tasks_data.keys():
        return Response(status=400, mimetype='application/json')
    elif task_id != num:
        return Response(status=400, mimetype='application/json')
    elif task_name != tasks_data[num]['result']['name']:
        return Response(status=400, mimetype='application/json')
    elif task_status == 0 or task_status == 1:

        tasks_data[num]['result']['status'] = task_status
        response = jsonify(tasks_data[num])
        print(tasks_data)
        return response
    else:
        return Response(status=400, mimetype='application/json')


@task_blue.route('/task/<int:num>', methods=['DELETE'])
def delete_task(num):
    global tasks_data_id
    global tasks_data

    try:
        tasks_data.pop(num)
        return Response(status=200, mimetype='application/json')

    except KeyError:
        return Response(status=400, mimetype='application/json')
