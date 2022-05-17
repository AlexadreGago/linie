#?simple module to check if 2 coordinates are in range and return the distance along with the boolean

import geopy.distance

def check(coords_1, coords_2, range):
    """
    Simple function to check if 2 coordinates are in range and return the distance
    
    Args:
        coords_1 (tuple): coordinates of the first point
        coords_2 (tuple): coordinates of the second point
        range (int): range of the coordinates
    :return: Returns the distance if the coordinates are in range, otherwise returns None
    :rtype: float/None
    """
    distance=geopy.distance.geodesic(coords_1, coords_2).km
    if distance < range:
        return distance
    else:
        return None