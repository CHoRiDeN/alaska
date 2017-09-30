import requests
import json

def flightMultiCall(dest1,dest2):
    r = {"requests": [
        {"to": "BCN", "flyFrom": dest1, "directFlights": 0, "dateFrom": "11/06/2017", "dateTo": "13/09/2017"},
        {"to": dest1, "flyFrom": dest2, "directFlights": 0, "dateFrom": "14/06/2017", "dateTo": "16/09/2017"},
        {"to": dest2, "flyFrom": "BCN", "directFlights": 0, "dateFrom": "17/06/2017", "dateTo": "19/09/2017"}
    ]}
    response = requests.post('https://api.skypicker.com/flights_multi?partner=picky&locale=es&curr=EUR', data = json.dumps(r), headers = {'Content-Type':'application/json'} )
    return response
