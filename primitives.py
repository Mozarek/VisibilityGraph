from sortUtil import *

class Obstacle:
    def __init__(self , points, id):
        self.points = points
        self.n = len(points)
        self.id = id

class Point:
    def __init__(self , coords , id , obstacle):
        self.coords = coords
        self.id = id
        self.obstacle = obstacle

    def __eq__(self , other):
        return self.id == other.id
        
class Edge:
    def __init__(self , p1 , p2):
        self.points = [p1,p2]
    
class TreeEdge:
    def __init__(self , p0, p1 , p2):
        self.orientPoint = p0
        self.points = [p1,p2]
    
    def __gt__(self, other):
        p0 = self.orientPoint.coords
        p1 = self.points[0].coords
        p2 = self.points[1].coords
        p3 = other.points[0].coords
        p4 = other.points[1].coords
        if(cross(p0, p1, p3, p4) or cross(p0, p2, p3, p4)):
            return True
        min1 = min(dist(p0, p1), dist(p0, p2))
        max1 = max(dist(p0, p1), dist(p0, p2))
        min2 = min(dist(p0, p3), dist(p0, p4))
        max2 = max(dist(p0, p3), dist(p0, p4))
        if(min2 < min1 and max2 < max1):
            return True
        return False

    def __lt__(self, other):
        p0 = self.orientPoint.coords
        p1 = self.points[0].coords
        p2 = self.points[1].coords
        p3 = other.points[0].coords
        p4 = other.points[1].coords
        if(cross(p1, p2, p3, p0) or cross(p1, p2, p4, p0)):
            return True
        min1 = min(dist(p0, p1), dist(p0, p2))
        max1 = max(dist(p0, p1), dist(p0, p2))
        min2 = min(dist(p0, p3), dist(p0, p4))
        max2 = max(dist(p0, p3), dist(p0, p4))
        if(min1 < min2 and max1 < max2):
            return True
        return False

    def __eq__(self, other):
        if(self is None or other is None):
            if(self is other):
                return True
            return False
        return(self.points[0] == other.points[0] and self.points[1] == other.points[1])