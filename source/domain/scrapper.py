import requests
import datetime
import json
from pymongo import MongoClient
import time

client = MongoClient(
    'database',
    27017)
db = client.tripsdb


def getCheapestRoute(availDest, origin,startDateFrom):
    cheapests = []
    maxRoutesPerDay = 3
    for dest1 in availDest:
        for dest2 in availDest:
            if dest1 is not dest2:
                response = flightMultiCall(dest1, dest2, origin, startDateFrom)

                try:
                    if len(response.json()['data']) > 0:
                        print('adding route')
                        cheapests.append(response.json()['data'][0])
                except:
                    print('Error for '+origin+'->'+dest1+'->'+dest2+'->'+origin)
                    print(response)
                    print(response.json())

    print('sorting')
    sortedFLights = sorted(cheapests, key=lambda k: k['price'])
    countRoutes = 0
    print(len(sortedFLights))
    print('Filtering...')
    for result in sortedFLights:
        print(result)
        if result['price'] < 100:
            print('found less than 100€')
            jumps = []
            for jump in result['route']:
                jumpInfo = {
                    'cityFrom': jump['route'][0]['cityFrom'],
                    'codeFrom': jump['route'][0]['flyFrom'],
                    'cityTo': jump['route'][0]['cityTo'],
                    'codeTo': jump['route'][0]['flyTo'],
                    'departureDatetime': jump['route'][0]['utc_departure'],
                    'arrivalDatetime': jump['route'][0]['utc_arrival'],
                    'flightNum': jump['route'][0]['flight_no'],
                    'airlineCode': jump['route'][0]['airline']
                }
                jumps.append(jumpInfo)
            item_doc = {
                'dateFrom': result['route'][0]['utc_departure'],
                'dateTo': result['route'][0]['utc_arrival'],
                'price': result['price'],
                'departure': result['route'][0]['route'][0]['cityFrom'],
                'destination1': result['route'][0]['route'][0]['cityTo'],
                'destination2': result['route'][1]['route'][0]['cityTo'],
                'arrival': result['route'][2]['route'][0]['cityTo'],
                'foundAt': datetime.datetime.now(),
                'jumps': jumps,
                'link': 'https://www.kiwi.com/en/booking?lang=en&currency=eur&booking_token=',
                'raw': result
            }
            print('saving route found')
            countRoutes = countRoutes+1
            inserted = db.tripsdb.insert_one(item_doc)
    return

def flightMultiCall(dest1,dest2,departure,dateFrom):
    print('checkin '+departure+' - '+dest1+' - '+dest2+' - '+departure+' on '+dateFrom.strftime("%d/%m/%Y"))
    url = "https://tequila-api.kiwi.com/v2/nomad?adults=1&sort=price&limit=10&date_from="+dateFrom.strftime("%d/%m/%Y")+"&date_to="+dateFrom.strftime("%d/%m/%Y")+"&fly_from="+departure+"&fly_to="+departure
    r = {
      "via": [
        {
          "locations": [
            dest1
          ],
          "nights_range": [
            1,
            2
          ]
        },
        {
          "locations": [
            dest2
          ],
          "nights_range": [
            1,
            2
          ]
        }
      ]
    }

    headers = {
      'accept': 'application/json',
      'apikey': 'OWV4CI2G2vXy3KyqVRxcFrmxqT_V0g9h',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(r))
    return response


#destinations = ['PRG','AMS','BER','LON','MIL','ROM','CPH','stockholm','PAR', 'OPO', 'MUC', 'RTM','BRU','DUB','WAW']
destinations = ['PRG','AMS','BER','LON','stockholm','PAR', 'OPO', 'MUC', 'RTM','BRU']
departure = 'BCN'
startDateFrom = datetime.datetime.now()
startDateFrom = startDateFrom + datetime.timedelta(days=65)

start = time.time()
for i in range(95):
    startDateFrom = startDateFrom + datetime.timedelta(days=1)
    getCheapestRoute(destinations,departure,startDateFrom)

end = time.time()
print('done')
print(end-start)

