import numpy as np

def detectIntersection(ray,seg):
    def getIntersectionPoint(seg1,seg2):
        xdiff = (seg1[0][0] - seg1[1][0], seg2[0][0] - seg2[1][0])
        ydiff = (seg1[0][1] - seg1[1][1], seg2[0][1] - seg2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception("lines",seg1,seg2, "do not intersect")

        d = (det(*seg1), det(*seg2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return (x, y)

    def on_segment(p1, p2, p):
        return min(p1[0], p2[0]) <= p[0] <= max(p1[0], p2[0]) and min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1])
    def ccw(a,b,c):
        """returns positive number when points a,b,c are counterclockwise , negative number when clockwise , 0 when collinear
           important to treat 0 as (-epsilon,epsilon) because of floating point arithmetic
        """
        return a[0]*b[1] + b[0]*c[1] + c[0]*a[1] - a[0]*c[1] - a[1]*b[0] - b[1]*c[0]

    def direction(p1, p2, p3):
        return  -ccw(p1,p2,p3)
    
    def dotProduct(p0, p1 , p2):
        v1 = [p1[0]-p0[0] , p1[1]-p0[1]]
        v2 = [p2[0]-p0[0] , p2[1]-p0[1]]
        return np.dot(v1,v2)
    
    p1,p2 = ray
    p3,p4 = seg
    # d1 = direction(p3, p4, p1)
    # d2 = direction(p3, p4, p2)
    d3 = direction(p1, p2, p3)
    d4 = direction(p1, p2, p4)

    if ((d3 >= 0 and d4 <= 0) or (d3 <= 0 and d4 >= 0)) and not (d3 == 0 and d4 == 0):
        point  = getIntersectionPoint(ray , seg)
        if dotProduct(p1,p2,point)>0:
            return point

    # elif d1 == 0 and on_segment(p3, p4, p1):
    #     return True
    # elif d2 == 0 and on_segment(p3, p4, p2):
    #     return True
    # elif d3 == 0 and on_segment(p1, p2, p3):
    #     return True
    # elif d4 == 0 and on_segment(p1, p2, p4):
    #     return True
    # else:
    
    return None