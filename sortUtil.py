from functools import cmp_to_key
import numpy as np

def sortedByAngleFromPoint(point , allPoints , epsilon):
    my_comp = Comparator(point , epsilon)
    points = sorted(allPoints , key = cmp_to_key(my_comp.mycmp))
    return points

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
    # print("locallyIntersects: ",p0, p, " ccw: ", ccw(p.prevP , p , p.nextP))
    # print("ccw1: ", ccw(p.prevP , p , p0))
    # print("ccw2:", ccw(p , p.nextP , p0))
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

def isEdgeCloser(edge1, edge2):
    def other(num):
        if num == 1:
            return 0
        return 1
    p0 = edge1.orientPoint
    min1 = min(distP(p0, edge1.points[0]), distP(p0, edge1.points[1]))
    max1 = max(distP(p0, edge1.points[0]), distP(p0, edge1.points[1]))
    min2 = min(distP(p0, edge2.points[0]), distP(p0, edge2.points[1]))
    max2 = max(distP(p0, edge2.points[0]), distP(p0, edge2.points[1]))
    if min1 < min2 and max1 < max2:
        return True
    for x in range(2):
        for y in range(2):
            if edge1.points[x] == edge2.points[y]:
                return distP(p0, edge1.points[other(x)]) < distP(p0, edge2.points[other(y)])
    return False

def epsEquals(p1, p2 , eps):
    return dist(p1,p2) < eps

def sgn(x, epsilon):
    if x < -epsilon:
        return -1
    if x > epsilon:
        return 1
    else:
        return 0

def cross(p1, p2, p3, p4):
    eps = 10**-10
    if(sgn(ccw(p1, p2, p3), eps)*sgn(ccw(p1, p2, p4), eps) < 0
    and sgn(ccw(p3, p4, p1), eps)*sgn(ccw(p3, p4, p2), eps) < 0):
        return True
    return False

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