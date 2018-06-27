import re
import json
import pickle

def to_decimal (loc):
    if type(loc) != str:
        loc = str(loc)
    if re.match('.*deg.*', loc):
        loc_list = re.split('[-deg\''']+', loc)
        if loc_list[0] == '':
            loc = float(loc_list[1]) + float(loc_list[2]) / 60 + float(loc_list[3]) / 3600
            return '-' + str(loc)
        return str(float(loc_list[0]) + float(loc_list[1]) / 60 + float(loc_list[2]) / 3600)
    return loc

def convert (feed):
    f = open(feed + '.json', 'r')
    jf = json.load(f)
    not_convert_f = open(feed + '_not_convert.txt', 'w')
    not_convert = [ ]
    for item in jf:
        lat = item['lat']
        lng = item['lng']
        try:
            lat = to_decimal(lat)
            item['location'] = [lat]
        except:
            not_convert.append(lat)
        try:
            lng = to_decimal(lng)
            item['location'].append(lng)
        except:
            not_convert.append(lng)
    f.close()
    f = open(feed + '.json', 'w')
    json.dump(jf, f)
    pickle.dump(not_convert, not_convert_f)
    f.close()
    not_convert_f.close()

if __name__ == '__main__':
    convert('test')
