from flask_restful import Resource
from resources.themes import themes
from domain.cheapestRouteUseCase import getCheapestRoute

class ThemesAction(Resource):
    def get(self):
        return themes

class RouteAction(Resource):
    def get(self):
        availDest = ['AMS','BER','MIL']
        cheapestRoute = getCheapestRoute(availDest,'BCN')
        return cheapestRoute