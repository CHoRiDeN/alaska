from flask import Flask
import requests
import json
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {
        'task': args['task'],
        'created_at': 'test'
        }
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

class TestAction(Resource):
    def get(self):
        r = {"requests": [
            {"to": "PRG", "flyFrom": "BCN", "directFlights": 0, "dateFrom": "11/06/2017", "dateTo": "13/06/2017"},
            {"to": "BCN", "flyFrom": "PRG", "directFlights": 0, "dateFrom": "12/06/2017", "dateTo": "15/06/2017"}
        ]}
        response = requests.post('https://api.skypicker.com/flights_multi?partner=picky&locale=es&curr=EUR', data = json.dumps(r), headers = {'Content-Type':'application/json'} )
        return response.json()

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(TestAction, '/test')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
