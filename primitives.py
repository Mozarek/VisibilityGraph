from sortUtil import *

class Obstacle:
    def __init__(self , points, id):
        self.points = points
        self.n = len(points)
        self.id = id

class Point:
    def __init__(self , coords , id , obstacle , prevP , nextP):
        self.coords = coords
        self.id = id
        self.obstacle = obstacle
        self.prevP = prevP
        self.nextP = nextP

    def __repr__(self):
        return "id: " + str(self.id) + ", coords: " + str(self.coords)

    def __eq__(self , other):
        return self.id == other.id
        
class Edge:
    def __init__(self , p1 , p2):
        self.points = [p1,p2]
    
class TreeEdge:
    def __init__(self , p0, p1 , p2):
        self.orientPoint = p0
        self.points = [p1,p2]
        self.pointCoords = [p1.coords , p2.coords]
    
    def __gt__(self, other):
        p0 = self.orientPoint
        p1 = self.points[0]
        p2 = self.points[1]
        p3 = other.points[0]
        p4 = other.points[1]
        if(cross(p0, p1, p3, p4) or cross(p0, p2, p3, p4)):
            return True
        return isEdgeCloser(other, self)
        
    def __ge__(self,other):
        return self > other or self == other

    def __le__(self,other):
        return self < other or self == other

    def __lt__(self, other):
        p0 = self.orientPoint
        p1 = self.points[0]
        p2 = self.points[1]
        p3 = other.points[0]
        p4 = other.points[1]
        if(cross(p1, p2, p3, p0) or cross(p1, p2, p4, p0)):
            return True
        return isEdgeCloser(self, other)

    def __eq__(self, other):
        if(self is None or other is None):
            if(self is other):
                return True
            return False
        return ((self.points[0] == other.points[0] and self.points[1] == other.points[1])
                or (self.points[0] == other.points[1] and self.points[1] == other.points[0]))
            
    def __repr__(self):
        return "E(P1: "+str(self.points[0])+" || P2: "+str(self.points[1])+")"
