import requests
import json
def getCheapestRoute(availDest, origin):
    cheapests = []
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
