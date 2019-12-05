from functools import cmp_to_key
import numpy as np


def sortedByAngleFromPoint(p0 , allPoints , epsilon):
    """sorts allPoints by angle relative to p0"""
    my_comp = Comparator(p0 , epsilon)
    points = sorted(allPoints , key = cmp_to_key(my_comp.mycmp))
    return points

class Comparator:
    def __init__(self, p0 , epsilon):
        self.p0=p0
        self.eps = epsilon

    def mycmp(self,a, b):                             
        det = ccw(self.p0 , b , a)
        if abs(det) < self.eps:
            if distP(self.p0 , b) < distP(self.p0 , a):
                return 1
            else:
                return -1
        else:
            return -det

def ccw(p1,p2,p3):
    """returns positive number when points p1,p2,p3 are counterclockwise , negative number when clockwise , 0 when collinear
       important to treat 0 as (-epsilon,epsilon) because of floating point arithmetic
    """
    a = p1.coords
    b = p2.coords
    c = p3.coords
    return a[0]*b[1] + b[0]*c[1] + c[0]*a[1] - a[0]*c[1] - a[1]*b[0] - b[1]*c[0]

def locallyIntersects(p0 , p , EPS):
    """checks if segment [p0 , p] locally at p intersects interior of obstacle that p belongs to
        IMPORTANT: it is assumed that obstacles' points are always given in counter-clockwise order
    """
    if p0 == p.nextP or p0 == p.prevP:
        return False
    if ccw(p.prevP , p , p.nextP) < -EPS:
        return ccw(p.prevP , p , p0) > EPS or ccw(p , p.nextP , p0) > EPS
    else:
        return ccw(p.prevP , p , p0) > EPS and ccw(p , p.nextP , p0) > EPS

def distP(p1 , p2):
    return np.square(p1.coords[0]-p2.coords[0]) + np.square(p1.coords[1]-p2.coords[1])

def dist(p1 , p2):
    return np.square(p1[0]-p2[0]) + np.square(p1[1]-p2[1])

def epsEquals(p1, p2 , eps):
    return dist(p1,p2) < eps

def sgn(x, epsilon):
    if x < -epsilon:
        return -1
    if x > epsilon:
        return 1
    else:
        return 0

def checkCross(seg1,seg2 , EPS):
    """checks if segments seg1 and seg2 intersect with given epsilon EPS"""

    def __on_segment(p1, p2, p):
        return min(p1[0], p2[0]) <= p[0] <= max(p1[0], p2[0]) and min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1])
    def __ccw(a,b,c):
        """returns positive number when points a,b,c are counterclockwise , negative number when clockwise , 0 when collinear
           important to treat 0 as (-epsilon,epsilon) because of floating point arithmetic
        """
        return a[0]*b[1] + b[0]*c[1] + c[0]*a[1] - a[0]*c[1] - a[1]*b[0] - b[1]*c[0]

    def __direction(p1, p2, p3):
        return  -__ccw(p1,p2,p3)

    p1 = seg1[0].coords
    p2 = seg1[1].coords
    p3 = seg2[0].coords
    p4 = seg2[1].coords

    
    d1 = __direction(p3, p4, p1)
    d2 = __direction(p3, p4, p2)
    d3 = __direction(p1, p2, p3)
    d4 = __direction(p1, p2, p4)

    if (((d1 > EPS and d2 < EPS) or (d1 < EPS and d2 > EPS)) and
        ((d3 > EPS and d4 < EPS) or (d3 < EPS and d4 > EPS))):
        return True

    elif abs(d1) <EPS and __on_segment(p3, p4, p1):
        return True
    elif abs(d2) <EPS and __on_segment(p3, p4, p2):
        return True
    elif abs(d3) < EPS and __on_segment(p1, p2, p3):
        return True
    elif abs(d4) < EPS and __on_segment(p1, p2, p4):
        return True
    else:
        return False