from flask import Blueprint, jsonify, request, Response
from marshmallow import Schema, fields, ValidationError

task_blue = Blueprint('tasks', __name__)

tasks_data_id = 1  # task start id
tasks_data = dict()  # task DB


class CreateSchema(Schema):
    name = fields.String(required=True)


class UpdateSchema(Schema):
    name = fields.String(required=True)
    status = fields.Boolean(required=True)
    id = fields.Integer(required=True)


@task_blue.route('/tasks', methods=['GET'])
def get_list_tasks():
    task_list = [{"id": i, "name": "name", "status": 0} for i in range(1, 2)]
    response = jsonify({'result': task_list})
    return response


@task_blue.route('/task', methods=['POST'])
def create_task():
    global tasks_data_id
    global tasks_data

    request_body = request.get_json(force=True)
    schema = CreateSchema()
    try:
        schema.load(request_body)
    except ValidationError as e:
        return jsonify({'result': e.messages}), 400

    task_name = request_body.get('name')
    tasks_data[tasks_data_id] = {'result': {'name': task_name, 'status': 0, 'id': tasks_data_id}}

    response = jsonify(tasks_data[tasks_data_id])
    response.status_code = 201
    tasks_data_id += 1

    return response


@task_blue.route('/task/<int:num>', methods=['PUT'])
def update_task(num):
    global tasks_data_id
    global tasks_data

    request_body = request.get_json(force=True)
    schema = UpdateSchema()
    try:
        schema.load(request_body)
    except ValidationError as e:
        return jsonify({'result': e.messages}), 400

    task_id = request_body.get('id')
    task_status = request_body.get('status')
    task_name = request_body.get('name')
    if task_status == "1" or task_status == "0":  # marshmallow thinking "1", "0" is bool
        return jsonify({"result": {"status": ["Not a valid boolean."]}}), 400

    if task_id == num and task_id <= tasks_data_id:
        if not tasks_data.get(task_id) is None and task_name == tasks_data.get(task_id).get('result').get('name'):
            tasks_data[task_id]['result']['status'] = task_status
            response = jsonify(tasks_data[num])
            return response
        else:
            return jsonify({'result': 'KeyError'}), 400

    else:
        return jsonify({'result': 'KeyError'}), 400


@task_blue.route('/task/<int:num>', methods=['DELETE'])
def delete_task(num):
    global tasks_data_id
    global tasks_data

    try:
        tasks_data.pop(num)
        return Response(status=200, mimetype='application/json')

    except KeyError as e:
        return jsonify({'result': 'KeyError'}), 400
