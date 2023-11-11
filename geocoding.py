import requests
import pandas as pd
import numpy as np
import re
import geopandas as gpd
import matplotlib.pyplot as plt
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_MAPS_API")
 
# load datasets and sample 100 rows from each dataset
df_hospital_addresses = pd.read_csv('https://raw.githubusercontent.com/stephe-hu/datasci_7_geospatial/main/datasets/assignment7_slim_hospital_addresses.csv')
hospital_addresses_sample = df_hospital_addresses.sample(100)
hospital_addresses_sample

df_hospital_coordinates = pd.read_csv('https://raw.githubusercontent.com/stephe-hu/datasci_7_geospatial/main/datasets/assignment7_slim_hospital_coordinates.csv')
hospital_coordinates_sample = df_hospital_coordinates.sample(100)
hospital_coordinates_sample

# geocoding
google_response = []

for index, row in hospital_addresses_sample.iterrows():
    address = row['ADDRESS']
    city = row['CITY']
    state = row['STATE']

    search = 'https://maps.googleapis.com/maps/api/geocode/json?address='

    location_raw = f"{address}, {city}, {state}"
    location_clean = urllib.parse.quote(location_raw)

    url_request_part1 = search + location_clean + '&key=' + api_key
    url_request_part1

    response = requests.get(url_request_part1)
    response_dictionary = response.json()

    lat_long = response_dictionary['results'][0]['geometry']['location']
    lat_response = lat_long['lat']
    lng_response = lat_long['lng']

    final = {'address': address, 'lat': lat_response, 'lng': lng_response}
    google_response.append(final)

    print(f'....finished with {address}')


df_geocode = pd.DataFrame(google_response)
df_geocode

# reverse geocoding
def reverse_geocode(address_here): 

    search = 'https://maps.googleapis.com/maps/api/geocode/json?address='

    location_raw = address_here
    location_clean = urllib.parse.quote(location_raw)

    url_request_part1 = search + location_clean + '&key=' + api_key
    url_request_part1

    response = requests.get(url_request_part1)
    response_dictionary = response.json()

    lat_long = response_dictionary['results'][0]['geometry']['location']
    lat_response = lat_long['lat']
    lng_response = lat_long['lng']

    final = {'address': address_here, 'lat': lat_response, 'lng': lng_response}

    return final 
df_reverse_geocode = pd.DataFrame(google_response)
df_reverse_geocode

reverse_geocode('5483 MOORETOWN ROAD')