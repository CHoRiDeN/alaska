from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from app.apiController import *

app = Flask(__name__)
CORS(app)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('task')

api.add_resource(RouteAction, '/route/<month>/<year>')
api.add_resource(ThemesAction, '/themes')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
