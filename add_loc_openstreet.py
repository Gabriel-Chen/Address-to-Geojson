import json
import os
import sys
from keys import google_map_key
import certifi
from geopy.geocoders import Nominatim
import urllib
import re

# certificate set up
def uo(args, **kwargs):
    return urllib.request.urlopen(args, cafile=certifi.where(), **kwargs)
geolocator = Nominatim()
geolocator.urlopen = uo 

def convert (feed):
    feed_in = feed + '.json'
    json_f = open(feed_in, 'r')
    reader = json.load(json_f)
    not_founded = [ ]
    for item in reader:
        street = item['Where is the issue? Provide street, municipality, and state (don\'t include your personal information)']
        municipio = item['municipio']
        state = item['estado']
        try:
            location = geolocator.geocode(street)
            print('success converted with street!')
            if re.match('.*México.*', location.address):
                lat = location.latitude
                lng = location.longitude
                item['lat'] = lat
                item['lng'] = lng
                print('added location!')
            else:
                 print('not mexico addr, now trying with whole address...')
                location = geolocator.geocode(str(street) + ", " + str(municipio) + ", " + str(state))
                if re.match('.*México.*', location.address):
                     lat = location.latitude
                    lng = location.longitude
                    item['lat'] = lat
                    item['lng'] = lng
                    print('success converted with street, municipio, state!')
                else:
                    print('not mexico addr for the whole addr...')
        except:
            print('no location found...')
    json_f.close()
    out_f = open(feed_in, encoding='latin-1', mode='w')
    json.dump(reader, out_f)
    out_f.close()
    not_founded_f = open(feed + '_no_location_return.txt', 'w')
    not_founded_f.write(str(not_founded))
    not_founded_f.close()

if __name__ == "__main__":
    convert('test')
