import json
from infrastructure.KiwiRepository import flightMultiCall
def getCheapestRoute(availDest, origin):
    cheapests = []
    for dest1 in availDest:
        for dest2 in availDest:
            if dest1 is not dest2:
                response = flightMultiCall(dest1,dest2)
                if len(response.json()) > 0:
                    cheapests.append(response.json()[0])
    sortedFLights = sorted(cheapests, key=lambda k: k['price'])
    return sortedFLights[0]
