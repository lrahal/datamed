import requests
import json
import urllib

base_url= 'https://maps.googleapis.com/maps/api/geocode/json?'

def get_geoloc():
    # Set up search parameters - address and API key
    parameters = {'address': 'Tuscany, Italy', 'key': AUTH_KEY}

    # urllib.parse.urlencode turns parameters into url
    print(f"{base_url}{urllib.parse.urlencode(parameters)}")

    r = requests.get(f"{base_url}{urllib.parse.urlencode(parameters)}")

    data = json.loads(r.content)
    # data.get("results")[0].get("geometry").get("location")
    return data