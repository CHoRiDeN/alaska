from flask_restful import Resource
from flask import jsonify
from resources.themes import themes
from domain.cheapestRouteUseCase import getCheapestRoute
from pymongo import MongoClient
from bson.json_util import dumps
from bson import json_util, ObjectId
import json

client = MongoClient(
    'database',
    27017)
db = client.tripsdb

class ThemesAction(Resource):
    def get(self):
        return 'test'

class RoutesAction(Resource):
    def get(self, month, year):
        pipeline = [
            {
                "$project": {
                    "month": {"$month": "$dateFrom"},
                    "year": {"$year": "$dateFrom"},
                    "dateFrom": 1,
                    'dateTo': 1,
                    'price': 1,
                    'departure': 1,
                    'destination1': 1,
                    'destination2': 1,
                    'arrival': 1,
                    'jumps': 1,
                    'foundAt': 1
                }
            },
            {"$match": {"month": int(month), "year": int(year)}}

        ]
        cursor = db.tripsdb.aggregate(pipeline)

        result = list(cursor)

        return json.loads(json_util.dumps(result))