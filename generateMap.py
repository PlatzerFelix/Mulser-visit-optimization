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

""" 
    normaly the cleint data would not include coordiates, but we can use the getCoords function to get them from the address
    
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
    }

for client in clients:
    address = clients[client]["address"]
    postalCode = clients[client]["postalCode"]
    clients[client]["coordinates"] = getCoords(address+ " " + postalCode)

print(clients)
 """


def generateMap(userName, clientName, avgMeetingTime, timeAtMainClient, maxDrivingTime):

    with open("clients.json", "r") as f:
        clients = json.load(f)

    for name in clients:
        clients[name]["ranking"] = rankClient(
            clients[name]["KundenVolumen"],
            datetime.datetime.strptime(clients[name]["LetzterBesuch"], "%d.%m.%Y").date(),
            clients[name]["aktiverVertrag"],
            clients[name]["offeneRechnung"],
            clients[name]["alterTore"],
            datetime.datetime.strptime(clients[name]["vertragsAblauf"], "%d.%m.%Y").date(),
        )
        print(clients[name]["ranking"])

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
        timePerDay = maxDrivingTime
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
            newTime = newRoute["duration"] + ((len(testToVisit)-2) * (int(avgMeetingTime)/60)) + (int(timeAtMainClient)/60)
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
        <b>Rang::</b> {data['ranking']}<br>
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
