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
        if(cross(self.points[0], self.orientPoint, other.points[0], other.points[1])
        or cross(self.points[1], self.orientPoint, other.points[0], other.points[1])):
            return True
        min1 = min(dist(self.orientPoint, self.points[0]), dist(self.orientPoint, self.points[1]))
        max1 = max(dist(self.orientPoint, self.points[0]), dist(self.orientPoint, self.points[1]))
        min2 = min(dist(self.orientPoint, other.points[0]), dist(self.orientPoint, other.points[1]))
        max2 = max(dist(self.orientPoint, other.points[0]), dist(self.orientPoint, other.points[1]))
        if(min2 < min1 and max2 < max1):
            return True
        return False

    def __lt__(self, other):
        if(cross(self.points[0], self.points[1], other.points[0], other.orientPoint)
        or cross(self.points[1], self.points[1], other.points[0], other.orientPoint)):
            return True
        min1 = min(dist(self.orientPoint, self.points[0]), dist(self.orientPoint, self.points[1]))
        max1 = max(dist(self.orientPoint, self.points[0]), dist(self.orientPoint, self.points[1]))
        min2 = min(dist(self.orientPoint, other.points[0]), dist(self.orientPoint, other.points[1]))
        max2 = max(dist(self.orientPoint, other.points[0]), dist(self.orientPoint, other.points[1]))
        if(min1 < min2 and max1 < max2):
            return True
        return False

    def __eq__(self, other):
        if(self == None or other == None):
            if(self == other):
                return True
            return False
        return(self.points[0] == other.points[0] and self.points[1] == other.points[1])