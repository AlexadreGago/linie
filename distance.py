#?simple module to check if 2 coordinates are in range and return the distance along with the boolean

import geopy.distance

def check(coords_1, coords_2, range):
    distance=geopy.distance.geodesic(coords_1, coords_2).km
    if distance < range:
        return (True, distance)
    else:
        return (False, distance)