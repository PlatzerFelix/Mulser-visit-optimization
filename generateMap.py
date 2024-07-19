import math
import folium
from shapely.geometry import Polygon
import random
import requests
import json
import polyline
import copy
from rankClient import rankClient
from getCoordsForAdress import getCoords
import datetime

#TODO store clients in json file and add leads (also in json file)

""" 
clients = [
    {
        "name": "Thomas Fischer",
        "email": "thomas.fischer@example.com",
        "tel": "9998887774",
        "address": "Via Dante Alighieri 30",
        "postalCode": "37121",
        "province": "Veneto",
        "country": "Italien",
        "KundenVolumen": 360000,
        "LetzterBesuch": datetime.date(2021, 9, 20),
        "offeneRechnung": False,
        "aktiverVertrag": False,
        "alterTore": 2,
        "vertragsAblauf": datetime.date(2024, 7, 19),
    },
    {
        "name": "Katharina Wolf",
        "email": "katharina.wolf@example.com",
        "tel": "9898989891",
        "address": "Piazza San Marco 1",
        "postalCode": "30124",
        "province": "Veneto",
        "country": "Italien",
        "KundenVolumen": 150000,
        "LetzterBesuch": datetime.date(2023, 2, 15),
        "offeneRechnung": True,
        "aktiverVertrag": True,
        "alterTore": 5,
        "vertragsAblauf": datetime.date(2025, 8, 1),
    },
    {
        "name": "Jessica Schwarz",
        "email": "jessica.schwarz@example.com",
        "tel": "4545454543",
        "address": "Via Mazzini 25",
        "postalCode": "37121",
        "province": "Veneto",
        "country": "Italien",
        "KundenVolumen": 800000,
        "LetzterBesuch": datetime.date(2022, 5, 30),
        "offeneRechnung": False,
        "aktiverVertrag": True,
        "alterTore": 10,
        "vertragsAblauf": datetime.date(2023, 10, 15),
    },
    {
        "name": "Sabine Keller",
        "email": "sabine.keller@example.com",
        "tel": "1112223333",
        "address": "Corso Buenos Aires 45",
        "postalCode": "20124",
        "province": "Lombardia",
        "country": "Italien",
        "KundenVolumen": 50000,
        "LetzterBesuch": datetime.date(2023, 7, 1),
        "offeneRechnung": True,
        "aktiverVertrag": False,
        "alterTore": 1,
        "vertragsAblauf": datetime.date(2026, 12, 31),
    },
    {
        "name": "Michael Schulz",
        "email": "michael.schulz@example.com",
        "tel": "2223334441",
        "address": "Piazza Bra 21",
        "postalCode": "37121",
        "province": "Veneto",
        "country": "Italien",
        "KundenVolumen": 1200000,
        "LetzterBesuch": datetime.date(2019, 12, 10),
        "offeneRechnung": False,
        "aktiverVertrag": True,
        "alterTore": 12,
        "vertragsAblauf": datetime.date(2022, 11, 20),
    },
]

for client in clients:
    address = clients[client]["address"]
    postalCode = clients[client]["postalCode"]
    clients[client]["coordinates"] = getCoords(address+ " " + postalCode)

print(clients)
 """


def generateMap(userName, clientName):  
    clients = {
        "Lorenzo Bianchi": {
            "email": "lorenzo.bianchi@example.com",
            "tel": "0361 2045653",
            "address": "Vico Giganti 149",
            "postalCode": "27020",
            "province": "Pavia",
            "country": "Italien",
            "KundenVolumen": 120000,
            "LetzterBesuch": datetime.date(2022, 9, 15),
            "offeneRechnung": True,
            "aktiverVertrag": False,
            "alterTore": 1,
            "vertragsAblauf": datetime.date(2023, 11, 10),
            "coordinates": "8.780240,45.137540",
        },
        "Giorgia Rinaldi": {
            "email": "giorgia.rinaldi@example.com",
            "tel": "0326 1610072",
            "address": "Via Torricelli 15",
            "postalCode": "38060",
            "province": "Trento",
            "country": "Italien",
            "KundenVolumen": 220000,
            "LetzterBesuch": datetime.date(2023, 3, 22),
            "offeneRechnung": False,
            "aktiverVertrag": True,
            "alterTore": 2,
            "vertragsAblauf": datetime.date(2025, 6, 18),
            "coordinates": "10.735736,46.068761",
        },
        "Federico Colombo": {
            "email": "federico.colombo@example.com",
            "tel": "0341 4259311",
            "address": "Corso Porta Borsari 14",
            "postalCode": "38060",
            "province": "Trento",
            "country": "Italien",
            "KundenVolumen": 300000,
            "LetzterBesuch": datetime.date(2021, 11, 11),
            "offeneRechnung": True,
            "aktiverVertrag": False,
            "alterTore": 3,
            "vertragsAblauf": datetime.date(2024, 4, 15),
            "coordinates": "10.935736,45.875436",
        },
        "Anna Moretti": {
            "email": "anna.moretti@example.com",
            "tel": "0374 4318387",
            "address": "Via San Domenico 45",
            "postalCode": "39040",
            "province": "Bolzano",
            "country": "Italien",
            "KundenVolumen": 250000,
            "LetzterBesuch": datetime.date(2022, 6, 28),
            "offeneRechnung": False,
            "aktiverVertrag": True,
            "alterTore": 2,
            "vertragsAblauf": datetime.date(2024, 10, 5),
            "coordinates": "11.190760,46.556473",
        },
        "Matilde Ferrara": {
            "email": "matilde.ferrara@example.com",
            "tel": "0373 5091813",
            "address": "Corso Casale 136",
            "postalCode": "01018",
            "province": "Viterbo",
            "country": "Italien",
            "KundenVolumen": 340000,
            "LetzterBesuch": datetime.date(2022, 8, 14),
            "offeneRechnung": True,
            "aktiverVertrag": False,
            "alterTore": 4,
            "vertragsAblauf": datetime.date(2023, 12, 25),
            "coordinates": "11.756524,42.610317",
        },
        "Sergio De Luca": {
            "email": "sergio.deluca@example.com",
            "tel": "0358 6867644",
            "address": "Discesa Gaiola 112",
            "postalCode": "85030",
            "province": "Potenza",
            "country": "Italien",
            "KundenVolumen": 400000,
            "LetzterBesuch": datetime.date(2021, 9, 5),
            "offeneRechnung": False,
            "aktiverVertrag": True,
            "alterTore": 3,
            "vertragsAblauf": datetime.date(2025, 11, 30),
            "coordinates": "15.804224,40.639163",
        },
        "Giulia Neri": {
            "email": "giulia.neri@example.com",
            "tel": "0365 2899332",
            "address": "Via delle Mura Gianicolensi 69",
            "postalCode": "81030",
            "province": "Caserta",
            "country": "Italien",
            "KundenVolumen": 500000,
            "LetzterBesuch": datetime.date(2022, 2, 18),
            "offeneRechnung": True,
            "aktiverVertrag": False,
            "alterTore": 5,
            "vertragsAblauf": datetime.date(2024, 5, 20),
            "coordinates": "13.983522,41.094764",
        },
        "Alessandro Fontana": {
            "email": "alessandro.fontana@example.com",
            "tel": "0357 7095723",
            "address": "Via del Caggio 61",
            "postalCode": "63031",
            "province": "Ascoli Piceno",
            "country": "Italien",
            "KundenVolumen": 280000,
            "LetzterBesuch": datetime.date(2023, 7, 3),
            "offeneRechnung": False,
            "aktiverVertrag": True,
            "alterTore": 2,
            "vertragsAblauf": datetime.date(2025, 8, 12),
            "coordinates": "13.692716,42.909473",
        },
        "Martina Rossi": {
            "email": "martina.rossi@example.com",
            "tel": "0395 2224279",
            "address": "Via Vico Ferrovia 145",
            "postalCode": "44040",
            "province": "Ferrara",
            "country": "Italien",
            "KundenVolumen": 150000,
            "LetzterBesuch": datetime.date(2023, 4, 14),
            "offeneRechnung": True,
            "aktiverVertrag": False,
            "alterTore": 1,
            "vertragsAblauf": datetime.date(2024, 7, 5),
            "coordinates": "11.614139,44.837304",
        },
        "Valentina Parisi": {
            "email": "valentina.parisi@example.com",
            "tel": "0312 7856413",
            "address": "Via Alessandro Manzoni 24",
            "postalCode": "27010",
            "province": "Pavia",
            "country": "Italien",
            "KundenVolumen": 320000,
            "LetzterBesuch": datetime.date(2023, 6, 5),
            "offeneRechnung": True,
            "aktiverVertrag": False,
            "alterTore": 2,
            "vertragsAblauf": datetime.date(2024, 8, 30),
            "coordinates": "9.158207,45.061733",
        },
        "Andrea Ricci": {
            "email": "andrea.ricci@example.com",
            "tel": "0354 1297786",
            "address": "Via delle Mura Gianicolensi 39",
            "postalCode": "81010",
            "province": "Caserta",
            "country": "Italien",
            "KundenVolumen": 270000,
            "LetzterBesuch": datetime.date(2021, 12, 28),
            "offeneRechnung": False,
            "aktiverVertrag": True,
            "alterTore": 2,
            "vertragsAblauf": datetime.date(2025, 1, 18),
            "coordinates": "13.941522,41.025764",
        },
        "Silvia Marino": {
            "email": "silvia.marino@example.com",
            "tel": "0352 5152369",
            "address": "Via Nicolai 76",
            "postalCode": "32013",
            "province": "Belluno",
            "country": "Italien",
            "KundenVolumen": 450000,
            "LetzterBesuch": datetime.date(2022, 5, 10),
            "offeneRechnung": True,
            "aktiverVertrag": False,
            "alterTore": 3,
            "vertragsAblauf": datetime.date(2024, 4, 22),
            "coordinates": "12.282844,46.249784",
        },
        "Alberto Greco": {
            "email": "alberto.greco@example.com",
            "tel": "0358 2194333",
            "address": "Via Acrone 44",
            "postalCode": "15030",
            "province": "Alessandria",
            "country": "Italien",
            "KundenVolumen": 330000,
            "LetzterBesuch": datetime.date(2023, 1, 25),
            "offeneRechnung": False,
            "aktiverVertrag": True,
            "alterTore": 4,
            "vertragsAblauf": datetime.date(2025, 5, 9),
            "coordinates": "8.617883,45.004862",
        },
        "Elisa Barone": {
            "email": "elisa.barone@example.com",
            "tel": "0310 2934516",
            "address": "Via Silvio Spaventa 42",
            "postalCode": "06020",
            "province": "Perugia",
            "country": "Italien",
            "KundenVolumen": 380000,
            "LetzterBesuch": datetime.date(2022, 10, 7),
            "offeneRechnung": True,
            "aktiverVertrag": False,
            "alterTore": 5,
            "vertragsAblauf": datetime.date(2024, 3, 14),
            "coordinates": "12.389578,43.112134",
        },
        "Michela De Santis": {
            "email": "michela.desantis@example.com",
            "tel": "0380 4543775",
            "address": "Via Nizza 145",
            "postalCode": "31049",
            "province": "Treviso",
            "country": "Italien",
            "KundenVolumen": 200000,
            "LetzterBesuch": datetime.date(2023, 8, 20),
            "offeneRechnung": False,
            "aktiverVertrag": True,
            "alterTore": 1,
            "vertragsAblauf": datetime.date(2024, 6, 10),
            "coordinates": "12.231078,45.668872",
        },
        "Dario Marino": {
            "email": "dario.marino@example.com",
            "tel": "0376 2784593",
            "address": "Via Lombardi 134",
            "postalCode": "24020",
            "province": "Bergamo",
            "country": "Italien",
            "KundenVolumen": 350000,
            "LetzterBesuch": datetime.date(2022, 7, 15),
            "offeneRechnung": True,
            "aktiverVertrag": False,
            "alterTore": 3,
            "vertragsAblauf": datetime.date(2023, 9, 25),
            "coordinates": "9.732162,45.694469",
        },
        "Sara Fontana": {
            "email": "sara.fontana@example.com",
            "tel": "0380 9288132",
            "address": "Via Loreto 7",
            "postalCode": "63020",
            "province": "Ascoli Piceno",
            "country": "Italien",
            "KundenVolumen": 260000,
            "LetzterBesuch": datetime.date(2023, 2, 27),
            "offeneRechnung": False,
            "aktiverVertrag": True,
            "alterTore": 2,
            "vertragsAblauf": datetime.date(2025, 3, 18),
            "coordinates": "13.609889,42.987991",
        },
        "Riccardo Morelli": {
            "email": "riccardo.morelli@example.com",
            "tel": "0321 2627322",
            "address": "Via Antonio Cecchi 93",
            "postalCode": "30033",
            "province": "Venezia",
            "country": "Italien",
            "KundenVolumen": 390000,
            "LetzterBesuch": datetime.date(2023, 6, 10),
            "offeneRechnung": True,
            "aktiverVertrag": False,
            "alterTore": 3,
            "vertragsAblauf": datetime.date(2024, 7, 30),
            "coordinates": "12.184719,45.491133",
        },
        "Chiara Rizzi": {
            "email": "chiara.rizzi@example.com",
            "tel": "0369 9312910",
            "address": "Via Moiariello 42",
            "postalCode": "12030",
            "province": "Cuneo",
            "country": "Italien",
            "KundenVolumen": 480000,
            "LetzterBesuch": datetime.date(2022, 9, 5),
            "offeneRechnung": False,
            "aktiverVertrag": True,
            "alterTore": 4,
            "vertragsAblauf": datetime.date(2025, 8, 1),
            "coordinates": "7.676164,44.602184",
        },
        "Luca Bianchi": {
            "email": "luca.bianchi@example.com",
            "tel": "0336 4937452",
            "address": "Via Longhena 49",
            "postalCode": "00054",
            "province": "Roma",
            "country": "Italien",
            "KundenVolumen": 500000,
            "LetzterBesuch": datetime.date(2022, 7, 19),
            "offeneRechnung": True,
            "aktiverVertrag": False,
            "alterTore": 4,
            "vertragsAblauf": datetime.date(2024, 5, 12),
            "coordinates": "12.296205,41.771311",
        },
        "Maria Rossi": {
            "email": "maria.rossi@example.com",
            "tel": "0360 9298062",
            "address": "Corso Porta Borsari 5",
            "postalCode": "38060",
            "province": "Trento",
            "country": "Italien",
            "KundenVolumen": 320000,
            "LetzterBesuch": datetime.date(2023, 1, 14),
            "offeneRechnung": False,
            "aktiverVertrag": True,
            "alterTore": 2,
            "vertragsAblauf": datetime.date(2025, 3, 25),
            "coordinates": "10.935736,45.875436",
        },
        "Elena Verdi": {
            "email": "elena.verdi@example.com",
            "tel": "0323 5695482",
            "address": "Via Nicola Mignogna 58",
            "postalCode": "80070",
            "province": "Napoli",
            "country": "Italien",
            "KundenVolumen": 270000,
            "LetzterBesuch": datetime.date(2022, 6, 30),
            "offeneRechnung": True,
            "aktiverVertrag": False,
            "alterTore": 1,
            "vertragsAblauf": datetime.date(2024, 9, 5),
            "coordinates": "13.8818242,40.748362",
        },
        "Paolo Giordano": {
            "email": "paolo.giordano@example.com",
            "tel": "0398 1396013",
            "address": "Via Giotto 111",
            "postalCode": "37010",
            "province": "Verona",
            "country": "Italien",
            "KundenVolumen": 360000,
            "LetzterBesuch": datetime.date(2023, 3, 20),
            "offeneRechnung": False,
            "aktiverVertrag": True,
            "alterTore": 3,
            "vertragsAblauf": datetime.date(2025, 6, 15),
            "coordinates": "10.726408,45.583354",
        },
        "Sofia De Angelis": {
            "email": "sofia.deangelis@example.com",
            "tel": "0328 9813536",
            "address": "Via Partenope 38",
            "postalCode": "47100",
            "province": "Forli",
            "country": "Italien",
            "KundenVolumen": 210000,
            "LetzterBesuch": datetime.date(2022, 8, 22),
            "offeneRechnung": True,
            "aktiverVertrag": False,
            "alterTore": 2,
            "vertragsAblauf": datetime.date(2024, 11, 20),
            "coordinates": "12.038402,44.221513",
        },
        "Gianni Lombardi": {
            "email": "gianni.lombardi@example.com",
            "tel": "0344 7205471",
            "address": "Viale Augusto 99",
            "postalCode": "73020",
            "province": "Lecce",
            "country": "Italien",
            "KundenVolumen": 440000,
            "LetzterBesuch": datetime.date(2023, 2, 5),
            "offeneRechnung": False,
            "aktiverVertrag": True,
            "alterTore": 3,
            "vertragsAblauf": datetime.date(2025, 7, 10),
            "coordinates": "18.295394,40.258563",
        },
    }
    for name in clients:
        clients[name]["ranking"] = rankClient(
            clients[name]["KundenVolumen"],
            clients[name]["LetzterBesuch"],
            clients[name]["aktiverVertrag"],
            clients[name]["offeneRechnung"],
            clients[name]["alterTore"],
            clients[name]["vertragsAblauf"],
        )

    rankings = ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"]

    print(f"Going from {userName} to {clientName}")
    api_key = "5b3ce3597851110001cf6248f5511359f0784bc69234d6f8afd2a3d6"
    headers = {
        "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
    }
    call = requests.get(
        f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={clients[userName]['coordinates']}&end={clients[clientName]['coordinates']}",
        headers=headers,
    )
    jsonData = json.loads(call.text)
    with open("return.json", "w") as file:
        json.dump(jsonData, file)
    polyPoints = jsonData["features"][0]["geometry"]["coordinates"]
    summary = jsonData["features"][0]["properties"]["summary"]
    driveDistance = summary["distance"]

    def haversine(lon1, lat1, lon2, lat2):
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))
        km = 6371 * c
        return km

    def calculate_distance(point1, point2):
        lon1, lat1 = map(float, point1.split(","))
        lon2, lat2 = map(float, point2.split(","))
        return haversine(lon1, lat1, lon2, lat2)

    def calcRoute(coordinates):
        routeBody = {
            "coordinates": [[float(x) for x in c.split(",")] for c in coordinates]
        }
        headers = {
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
            "Authorization": f"Bearer {api_key}",
        }
        try:
            call = requests.post(
                f"https://api.openrouteservice.org/v2/directions/driving-car",
                headers=headers,
                json=routeBody,
            )
            call.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            callJson = call.json()

            summary = callJson["routes"][0]["summary"]
            poly = callJson["routes"][0]["geometry"]
            points = polyline.decode(poly)

            return {
                "duration": round(summary["duration"] / 60 / 60, 2),
                "distance": summary["distance"],
                "points": points,
            }
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Print the HTTP error
            print(
                f"Response from the API: {call.text}"
            )  # Print the whole response from the API
        except Exception as err:
            print(f"Other error occurred: {err}")  # Print any other errors
            print(
                f"Response from the API: {call.text}"
            )  # Print the whole response from the API if available

    lon_user, lat_user = map(float, clients[userName]["coordinates"].split(","))
    lon_client, lat_client = map(float, clients[clientName]["coordinates"].split(","))

    m = folium.Map(location=[lat_user, lon_user], zoom_start=6)

    i = 0
    min_radius_km = 20
    max_radius_km = driveDistance / 1000 / (4 * 2)
    num_points = len(polyPoints)

    # Calculate the midpoint
    midpoint = num_points // 2

    # Function to calculate the radius based on the index
    def calculate_radius(index, midpoint, min_radius_km, max_radius_km):
        if index <= midpoint:
            return (
                min_radius_km * 1000
                + (index / midpoint) * (max_radius_km - min_radius_km) * 500
            )
        else:
            return (
                min_radius_km * 1000
                + ((num_points - index) / midpoint)
                * (max_radius_km - min_radius_km)
                * 500
            )

    clients_within_circles = set()

    for point in polyPoints:
        if i % 15 == 0:
            radius = calculate_radius(i, midpoint, min_radius_km, max_radius_km)
            circle_center = (point[1], point[0])
            # folium.Circle(circle_center,radius).add_to(m)
            for client, data in clients.items():
                lon_client, lat_client = map(float, data["coordinates"].split(","))
                if (
                    calculate_distance(f"{point[0]},{point[1]}", data["coordinates"])
                    * 1000
                    <= radius
                ):
                    clients_within_circles.add(client)
        i += 1

    rankedclients = {}
    for client in clients_within_circles:
        rankedclients[client] = clients[client]["ranking"]
    rank_position = {rank: index for index, rank in enumerate(rankings)}

    sorted_clients = sorted(
        rankedclients.items(), key=lambda item: rank_position[item[1]]
    )

    sorted_clients_dict = dict(sorted_clients)
    print(sorted_clients_dict)
    toVisit = [clients[userName]["coordinates"], clients[clientName]["coordinates"]]
    toVisitclients = [userName, clientName]
    if len(clients_within_circles) > 2:
        timePerDay = 10
        overMax = 2
        currentOver = 0
        optimalRoute = None
        for client in sorted_clients_dict:
            if client == clientName or client == userName:
                continue
            if currentOver >= overMax:
                break
            testToVisit = copy.copy(toVisit)
            testToVisit.insert(-1, clients[client]["coordinates"])
            newRoute = calcRoute(testToVisit)
            newTime = newRoute["duration"] + len(testToVisit)
            if newTime < timePerDay:
                toVisit = copy.copy(testToVisit)
                toVisitclients.insert(-1, client)
                optimalRoute = copy.copy(newRoute)
                print(
                    f"Visiting client \033[92m{client} \033[0mwhich will take {math.floor(newTime)}h {round(newTime%60)} min. All stops: {toVisitclients}"
                )
            else:
                print(
                    f"Can not visit client \033[91m{client} \033[0mwhich would take {math.floor(newTime)}h {round(newTime%60)} min. All stops: {toVisitclients}"
                )
            if timePerDay - newTime < 1:
                currentOver += 1
    else:
        optimalRoute = calcRoute(
            [clients[userName]["coordinates"], clients[clientName]["coordinates"]]
        )
    if len(toVisitclients) <= 2:
        optimalRoute = calcRoute(
            [clients[userName]["coordinates"], clients[clientName]["coordinates"]]
        )

    def add_client_marker(client, data, index):
        lon_client, lat_client = map(float, data["coordinates"].split(","))
        popup_html = f"""
        <div style="font-size: 14px;">
        <strong>{client}</strong><br>
        <b>Email:</b> {data['email']}<br>
        <b>Tel:</b> {data['tel']}<br>
        <b>Adresse:</b> {data['address']}<br>
        <b>Postleitzahl:</b> {data['postalCode']}<br>
        <b>Provinz:</b> {data['province']}<br>
        <b>Land:</b> {data['country']}<br>
        <b>Kundenvolumen:</b> {data['KundenVolumen']}<br>
        <b>Letzter Besuch:</b> {data['LetzterBesuch']}<br>
        <b>Offene Rechnung:</b> {"Ja" if data['offeneRechnung'] else "Nein"}<br>
        <b>Aktiver Vertrag:</b> {"Ja" if data['aktiverVertrag'] else "Nein"}<br>
        <b>Alter der Tore:</b> {data['alterTore']} Jahre<br>
        <b>Vertragsablauf:</b> {data['vertragsAblauf']}<br>
        </div>
        """

        folium.Marker(
            [lat_client, lon_client],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=client,
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    font-size: 16px; 
                    color: white; 
                    background-color: green; 
                    border-radius: 50%; 
                    width: 24px; 
                    height: 24px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center;
                    text-align: center;">
                    {index+1}
                </div>
                """
            ),
        ).add_to(m)

    # Loop through clients to visit and add markers
    for i, client in enumerate(toVisitclients):
        data = clients[client]
        print(f"{client} @ {data['coordinates']}")
        add_client_marker(client, data, i)

    points = optimalRoute["points"]
    folium.PolyLine(
        locations=[[x[0], x[1]] for x in points],
        color="red",
        weight=4,
        opaclient=1,
    ).add_to(m)
    m.save("templates/output.html")
