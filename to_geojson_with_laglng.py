import json
import certifi
from geopy.geocoders import Nominatim
import urllib
import re

# certificate set up
def uo(args, **kwargs):
    return urllib.request.urlopen(args, cafile=certifi.where(), **kwargs)
geolocator = Nominatim()
geolocator.urlopen = uo 

def validate_loc (data):
    after = [ ]
    for item in data:
        address = geolocator.reverse(str(item['LATITUD']) + ', ' + str(item['LONGITUD']))
        if re.match('.*México.*', address.address):
            after.append(item)
            print('item added into the list')
        else:
            print(address.address)
            print('not mexico loc, item passed...')
    return after

def validate (data) :
    after = [ ]
    for item in data:
        try:
            loc = item['location']
            lat = loc[0]
            lng = loc[1]
            if float(lat) < 0:
                lat = str( - float(lat))
            if float(lng) > 0:
                lng = '-' + lng
            after.append(item)
        except:
            pass
    return after

def convert (feed):
    f = open(feed + '.json', 'r')
    jf = json.load(f)
    jf = validate(jf)
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type" : 
                "Feature",
                "geometry" : {
                    
                    "type": "Point",
                    "coordinates": [float(item['location'][1]), float(item['location'][0])],
                    },
                "properties" : item,
            } for item in jf
        ]
    }
    f.close()
    f = open(feed + '.geojson', encoding='latin-1', mode='w')
    json.dump(geojson, f)
    f.close()

if __name__ == "__main__":
    convert('datosRETC')
