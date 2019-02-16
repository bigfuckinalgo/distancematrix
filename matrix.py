import requests
import pdb
import json
import csv
from secrets import bing_maps_key

KEY = bing_maps_key

def read_latlongs_json():
    latlongs_from_file = []

    with open("kl_b-junioren_niedersachsen.json", "r") as f:
        data = json.load(f)
        import os
        filename = os.path.basename(f.name)
        name = os.path.splitext(filename)[0]

        for line in data:
            latlongs_from_file.append([float(line['lat']), float(line['lng'])])
    return latlongs_from_file, name # [0:10]

def get_distance_matrix(latlongs):
# We go over all the latlongs in the array except the last one - because then we are already done!
    dm_json = { 'data': [] }

    for index, oll in enumerate(latlongs[:-1]):
        # We want to calculate the distances from the current element to all subsequent ones in the array.
        origin_lat = oll[0]
        origin_long = oll[1]

        destinations = []

        for dest_ll in latlongs[index+1:]:
            dest_lat = dest_ll[0]
            dest_long = dest_ll[1]
            destinations.append({"latitude": dest_lat, "longitude": dest_long})

        post_json = {'origins': [{"latitude": origin_lat, "longitude": origin_long}],
            'destinations': destinations,
            'travelMode': "driving"
         }

        params = {
             'key': KEY
        }

        r = requests.post('https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix',
            params=params, json=post_json)
        r_json = r.json()

        print(json.dumps(r.json(), indent=4))

        # Usually this should be redundant, same as the destinations above,
        # but just in case they are given back in a different order ...
        r_destinations = r_json['resourceSets'][0]['resources'][0]['destinations']
        r_distances = r_json['resourceSets'][0]['resources'][0]['results']

        for r_d_d in zip(r_destinations, r_distances):
            # pdb.set_trace()
            origin_lat_long = ",".join(str(x) for x in oll)
            destination_lat_long = ",".join(str(x) for x in r_d_d[0].values())

            destination_lat = r_d_d[0]['latitude']
            destination_long = r_d_d[0]['longitude']

            distance = r_d_d[1]['travelDistance']
            duration = r_d_d[1]['travelDuration']

            # ['origin_lat_long', 'destination_lat_long', 'travel_time', 'travel_distance']
            # file_writer.writerow([origin_lat_long, destination_lat_long, duration, distance])
            dm_json['data'] = dm_json['data'] + [{'origin_lat': origin_lat, 'origin_long': origin_long,
                'destination_lat': destination_lat, 'destination_long': destination_long,
                'duration': duration, 'distance': distance}]
    return dm_json

latlongs_array, name = read_latlongs_json()

# csv_file_name = "{}_distances.csv".format(name)
json_file_name = "{}_distances.json".format(name)

# with open(csv_file_name, mode='w+') as file:
#    file_writer = csv.writer(file, delimiter='|')
#    file_writer.writerow(['origin_lat_long', 'destination_lat_long', 'travel_time', 'travel_distance'])

dm_json = get_distance_matrix(latlongs_array)

with open(json_file_name, mode='w+') as jsonfile:
    json.dump(dm_json, jsonfile, indent = 4)
