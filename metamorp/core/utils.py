'''
Created on Apr 24, 2014

@author: igor
'''

def point_inside_polygon(x, y, poly):
    '''
    Taken from http://www.ariel.com.au/a/python-point-int-poly.html
    Args:
        x, y (int): Coordinate for the point to test
        poly (list of int): A list of polygon points coordinates 
            in the form [px1, py1, px2, py2,....]
    '''
    n = len(poly)
    inside = False
    p1x = poly[0]
    p1y = poly[1]
    for i in range(0, n + 2, 2):
        p2x = poly[i % n]
        p2y = poly[(i + 1) % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside