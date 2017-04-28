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

        cheapests = []
        availDest = ['AMS','BER','MIL','PAR','MUC','OSL']
        for dest1 in availDest:
            for dest2 in availDest:
                if dest1 is not dest2:
                    r = {"requests": [
                        {"to": dest1, "flyFrom": "BCN", "directFlights": 0, "dateFrom": "11/06/2017", "dateTo": "13/06/2017"},
                        {"to": dest2, "flyFrom": dest1, "directFlights": 0, "dateFrom": "14/06/2017", "dateTo": "16/06/2017"},
                        {"to": "BCN", "flyFrom": dest2, "directFlights": 0, "dateFrom": "17/06/2017", "dateTo": "19/06/2017"}
                    ]}
                    response = requests.post('https://api.skypicker.com/flights_multi?partner=picky&locale=es&curr=EUR', data = json.dumps(r), headers = {'Content-Type':'application/json'} )
                    if len(response.json()) > 0:
                        cheapests.append(response.json()[0])
        sortedFLights = sorted(cheapests, key=lambda k: k['price'])
        return sortedFLights[0]


##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(TestAction, '/test')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
