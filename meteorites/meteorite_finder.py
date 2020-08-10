import requests
import math

def find_nearest_meteors():
    m = get_meteorite_dists()
    m.sort(key=sort_key)
    print("The nearest meteor landings to me are:\n")
    i = 0
    while i < 10:
        print("{0}: Which {2} {1}km away at {3}\n".format(m[i]['name'],m[i]['distance'],m[i]['fall'],m[i]['geo']))
        i += 1

def local_haversine(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * \
        math.sin((lon2 - lon1) / 2) ** 2

    r = 6372.8 # Radius of the earth

    return 2 * r * math.asin(math.sqrt(h))

def get_meteorite_dists():
    resp = requests.get("https://data.nasa.gov/resource/gh4g-9sfh.json")
    meteorites = resp.json()
    home_loc = (-31.9554838, 115.8992903)
    mfh = []
    for m in meteorites:
        try:
            m_loc = (float(m['reclat']),float(m['reclong']))
            m_dist = local_haversine(home_loc[0], home_loc[1], m_loc[0], m_loc[1])
            mfh += [{'name': m['name'], 'distance': m_dist, 'fall': m['fall'], 'geo': m['geolocation']}]
        except KeyError:
            continue
    return mfh

def sort_key(e):
    return e['distance']

find_nearest_meteors()
