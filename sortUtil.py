from functools import cmp_to_key
import numpy as np

def sortedByAngleFromPoint(point , allPoints , epsilon):
    my_comp = Comparator(point , epsilon)
    points = sorted(allPoints , key = cmp_to_key(my_comp.mycmp))
    return points

def ccw(a,b,c):
    """returns positive number when points a,b,c are counterclockwise , negative number when clockwise , 0 when collinear
       important to treat 0 as (-epsilon,epsilon) because of floating point arithmetic
    """
    return a[0]*b[1] + b[0]*c[1] + c[0]*a[1] - a[0]*c[1] - a[1]*b[0] - b[1]*c[0]

def dist(p1 , p2):
    return np.square(p1[0]-p2[0]) + np.square(p1[1]-p2[1])

def sgn(x, epsilon):
    if x < -epsilon:
        return -1
    if x > epsilon:
        return 1
    else:
        return 0

def cross(p1, p2, p3, p4):
    eps = 10**-10
    if(sgn(ccw(p1, p2, p3), eps)*sgn(ccw(p1, p2, p4), eps) <= 0
    and sgn(ccw(p3, p4, p1), eps)*sgn(ccw(p3, p4, p2), eps) <= 0):
        return True
    return False

""" not working but not needed
def crossPoint(p1, p2, p3, p4):
    xdiff = (p1[0] - p2[0], p3[0] - p4[0])
    ydiff = (p1[1] - p2[1], p3[1] - p4[1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
"""

class Comparator:
    def __init__(self, p0 , epsilon):
        self.p0=p0
        self.eps = epsilon

    def mycmp(self,a, b):                             
        det = ccw(self.p0.coords , b.coords , a.coords)
        if abs(det) < self.eps:
            if dist(self.p0.coords , b.coords) < dist(self.p0.coords , a.coords):
                return 1
            else:
                return -1
        else:
            return det