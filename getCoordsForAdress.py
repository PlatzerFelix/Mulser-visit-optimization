import requests
import json
def getCoords(address):
    headers = {
        "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
    }
    try:
        call = requests.post(
            f"https://api.openrouteservice.org/geocode/search?api_key=5b3ce3597851110001cf6248f5511359f0784bc69234d6f8afd2a3d6&text={address}&size=1",
            headers=headers,
        )
        call.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        callJson = call.json()
        return callJson["features"][0]["geometry"]["coordinates"]
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
