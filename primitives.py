from sortUtil import *
from rayLineIntersection import detectRaySegIntersection

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
        return self != other and not self < other
        
    def __ge__(self,other):
        return self > other or self == other

    def __le__(self,other):
        return self < other or self == other

    def __lt__(self, other):
        EPS = 1e-5
        p0 = self.orientPoint
        p1 = self.points[0]
        p2 = self.points[1]
        p3 = other.points[0]
        p4 = other.points[1]
        if p1 != p3 and p1 != p4:
            if checkCross([p0, p1] , [p3,p4] , EPS):
                return False
            elif detectRaySegIntersection([p0,p1],[p3,p4],EPS):
                return True
        
        if p2!=p3 and p2!=p4:
            if checkCross([p0, p2] , [p3,p4] , EPS):
                return False
            elif detectRaySegIntersection([p0,p2],[p3,p4],EPS):
                return True
        
        if p3!=p1 and p3!=p2:
            if checkCross([p0, p3] , [p1,p2] , EPS):
                return True
            elif detectRaySegIntersection([p0,p3],[p1,p2],EPS):
                return False
        
        if p4!=p1 and p4!=p2:
            if checkCross([p0, p4] , [p1,p2] , EPS):
                return True
            elif detectRaySegIntersection([p0,p4],[p1,p2],EPS):
                return False

        raise Exception("Edges: " , self , " " , other , ", cannot be compared\n  with respect to: " , p0)


    def __eq__(self, other):
        if(self is None or other is None):
            if(self is other):
                return True
            return False
        return ((self.points[0] == other.points[0] and self.points[1] == other.points[1])
                or (self.points[0] == other.points[1] and self.points[1] == other.points[0]))
            
    def __repr__(self):
        return "E(P1: "+str(self.points[0])+" || P2: "+str(self.points[1])+")"
