import requests
import requests
import datetime
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
import time

client = MongoClient(
    'alaska-database',
    27017)
db = client.tripsdb


def getCheapestRoute(availDest, origin,startDateFrom):
    cheapests = []
    maxRoutesPerDay = 5
    for dest1 in availDest:
        for dest2 in availDest:
            if dest1 is not dest2:
                response = flightMultiCall(dest1, dest2, origin, startDateFrom)
                try:
                    if len(response.json()) > 0:
                        cheapests.append(response.json()[0])
                except:
                    print('Error for '+origin+'->'+dest1+'->'+dest2+'->'+origin)
                    print(response)

    sortedFLights = sorted(cheapests, key=lambda k: k['price'])
    countRoutes = 0
    for route in sortedFLights:
        if route['price'] < 100 and countRoutes < maxRoutesPerDay:
            departureDateEpoch = route['route'][0]['dTimeUTC']
            departureDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(departureDateEpoch))
            departureDateTime = datetime.datetime.strptime(departureDateTime, '%Y-%m-%d %H:%M:%S')
            arrivalDateEpoch = route['route'][2]['aTimeUTC']
            arrivalDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(arrivalDateEpoch))
            arrivalDateTime = datetime.datetime.strptime(arrivalDateTime, '%Y-%m-%d %H:%M:%S')
            jumps = []
            for jump in route['route']:
                jumpInfo = {
                    'cityFrom': jump['route'][0]['cityFrom'],
                    'codeFrom': jump['route'][0]['flyFrom'],
                    'cityTo': jump['route'][0]['cityTo'],
                    'codeTo': jump['route'][0]['flyTo'],
                    'departureDatetime': jump['route'][0]['dTime'],
                    'arrivalDatetime': jump['route'][0]['aTime'],
                    'departureLocation': {
                        'lng': jump['route'][0]['lngFrom'],
                        'lat': jump['route'][0]['latFrom'],
                    },
                    'arrivalLocation': {
                        'lng': jump['route'][0]['lngTo'],
                        'lat': jump['route'][0]['latTo'],
                    },
                    'flightNum': jump['route'][0]['flight_no'],
                    'airlineCode': jump['route'][0]['airline']
                }
                jumps.append(jumpInfo)
            item_doc = {
                'dateFrom': departureDateTime,
                'dateTo': arrivalDateTime,
                'price': route['price'],
                'departure': route['route'][0]['route'][0]['cityFrom'],
                'destination1': route['route'][0]['route'][0]['cityTo'],
                'destination2': route['route'][1]['route'][0]['cityTo'],
                'arrival': route['route'][2]['route'][0]['cityTo'],
                'foundAt': datetime.datetime.now(),
                'jumps': jumps,
                'raw': route
            }
            print('saving route found')
            countRoutes = countRoutes+1
            inserted = db.tripsdb.insert_one(item_doc)
    return sortedFLights[0]

def flightMultiCall(dest1,dest2,departure,dateFrom):
    date2 = dateFrom + datetime.timedelta(days=1)
    date3 = date2 + datetime.timedelta(days=1)
    date4 = date3 + datetime.timedelta(days=1)
    date5 = date4 + datetime.timedelta(days=1)
    date6 = date5 + datetime.timedelta(days=1)
    r = {"requests": [
        {"to": dest1, "flyFrom": departure, "directFlights": 1, "dateFrom": dateFrom.strftime("%d/%m/%Y"), "dateTo": date2.strftime("%d/%m/%Y")},
        {"to": dest2, "flyFrom": dest1, "directFlights": 1, "dateFrom": date3.strftime("%d/%m/%Y"), "dateTo": date4.strftime("%d/%m/%Y")},
        {"to": departure, "flyFrom": dest2, "directFlights": 1, "dateFrom": date5.strftime("%d/%m/%Y"), "dateTo": date6.strftime("%d/%m/%Y")}
    ]}
    response = requests.post('https://api.skypicker.com/flights_multi?partner=picky&locale=es&curr=EUR', data = json.dumps(r), headers = {'Content-Type':'application/json'} )
    return response

destinations = ['MIL','AMS','BER','LON','ROM','DBV','BUD']
departure = 'BCN'
startDateFrom = datetime.datetime.now()
startDateFrom = startDateFrom + datetime.timedelta(days=45)

start = time.time()
for i in range(100):
    startDateFrom = startDateFrom + datetime.timedelta(days=1)
    getCheapestRoute(destinations,departure,startDateFrom)

end = time.time()
print('done')
print(end-start)

