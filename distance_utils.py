import openrouteservice
import pandas as pd
import time
import streamlit as st

client = openrouteservice.Client(key=st.secrets["ORS_API_KEY"])

def get_coordinates(place):
    try:
        result = client.pelias_search(text=place)
        return result['features'][0]['geometry']['coordinates']
    except:
        return None

def get_distance_km(loc_a, loc_b):
    origin = get_coordinates(loc_a)
    destination = get_coordinates(loc_b)

    if not origin or not destination:
        return "Error"

    try:
        route = client.directions(
            coordinates=[origin, destination],
            profile='driving-car',
            format='geojson'
        )
        distance_m = route['features'][0]['properties']['segments'][0]['distance']
        return round(distance_m / 1000, 2)
    except:
        return "Error"
