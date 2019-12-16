import numpy as np
from sortUtil import *
from primitives import *
from rbTree import RedBlackTree
from visualizationPrimitives import *
from rayLineIntersection import detectRaySegIntersection

class VisibilityGraph:
    def __init__(self , obstaclePoints):
        '''obstaclePoints is a list of lists of points - each representing one obstacle'''
        obstacles = list()
        vertices = list()

        p_id=0
        for o_id , o in enumerate(obstaclePoints):
            newVertices = list()
            for p in o:
                newVertices.append(Point(p,p_id, o , None , None))
                p_id+=1
            for i,p in enumerate(o):
                newVertices[i].nextP = newVertices[(i+1)%len(o)]
                newVertices[i].prevP = newVertices[(i+len(o)-1)%len(o)]
            vertices.extend(newVertices)
            obstacles.append(Obstacle(newVertices ,o_id))
        self.vertices = vertices
        self.obstacles = obstacles
        self.scenes = list([])

    def calculateVisibilityGraph(self):
        G = [list() for v in self.vertices]
        E = list()

        for p in self.vertices:
            w = self.__visibleVerticesFrom(p)
            for visibleP in w:
                if p.id < visibleP.id:
                    G[p.id].append(visibleP)
                    G[visibleP.id].append(p)
                    E.append([p , visibleP])
        
        self.scenes.append(createFinalScene(E))

        return (G,E)


    def __visibleVerticesFrom(self , p0):
        """returns a list of Point objects visible from p0"""
        EPS = 1e-10
        sortedPoints = sortedByAngleFromPoint(p0 , self.vertices , EPS)

        #initialize tree
        rbT = RedBlackTree()
        visibleVertices = []

        rayFrom = p0
        rayTo = sortedPoints[1]
        #add all edges that intersect the ray in its initial position [rayFrom , rayTo]
        for p in sortedPoints[1:]:
            
            intersectionPoint = detectRaySegIntersection([rayFrom , rayTo] , [p , p.nextP] , EPS)
            if intersectionPoint != None:
                if epsEquals(intersectionPoint, p.coords, EPS) or epsEquals(intersectionPoint, p.nextP.coords, EPS):
                    pointOn = p
                    other = p.nextP
                    if epsEquals(intersectionPoint, p.nextP.coords, EPS):
                        (other,pointOn) = (pointOn,other)

                    if ccw(rayFrom , pointOn , other) > EPS:
                        rbT.add(TreeEdge(rayFrom , p , p.nextP))
                else:
                    rbT.add(TreeEdge(rayFrom , p , p.nextP))
        
        self.scenes.append(createScene(rbT , [rayFrom,rayTo] , visibleVertices))

        #main loop
        previous = None
        for p in sortedPoints[1:]:
            if self.__visible(p0 , previous , visibleVertices , p , rbT):
                visibleVertices.append(p)

            if ccw(p0 , p , p.nextP) > EPS:
                rbT.remove(TreeEdge(p0 , p , p.nextP))
            if ccw(p0 , p , p.prevP) > EPS:
                rbT.remove(TreeEdge(p0 , p , p.prevP))
            
            if ccw(p0, p, p.nextP) < -EPS:
                rbT.add(TreeEdge(p0, p, p.nextP))
            if ccw(p0, p, p.prevP) < -EPS:
                rbT.add(TreeEdge(p0, p, p.prevP))
            previous = p
            self.scenes.append(createScene(rbT , [rayFrom,p] , visibleVertices))

        return visibleVertices

    def __visible(self, p0, previous , visibleVertices, point , rbT):
        def __existsEdgeBetween(p1, p2):
            print("edge between called")
            if(distP(p0, p1) < distP(p0, p2)):
                nearPoint = p1
                farPoint = p2
            else:
                nearPoint = p2
                farPoint = p1
            e1 = rbT.successor(TreeEdge(p0, nearPoint, nearPoint.nextP))
            if e1 == TreeEdge(p0 , nearPoint , nearPoint.prevP):
                e1 = rbT.successor(e1)
            ek1 = TreeEdge(p0, farPoint, farPoint.nextP)
            ek2 = TreeEdge(p0, farPoint, farPoint.prevP)
            return e1 != None and e1 != ek1 and e1 != ek2

        EPS = 1e-10
        """ checks if point is visible from p0 """
        if locallyIntersects(p0 , point , EPS):
            return False
        elif previous is None or abs(ccw(p0 , previous, point)) > EPS:
            e = rbT.findLeftmostValue()
            if (e is not None and e.points[0] != point and e.points[1] != point 
                and checkCross([p0, point], e.points, EPS)):
                return False
            else:
                return True
        else:
            if len(visibleVertices)>0 and previous != visibleVertices[-1]:
                return False
            else:
                return not __existsEdgeBetween(previous, point)