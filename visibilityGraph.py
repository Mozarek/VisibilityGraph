import numpy as np
from sortUtil import sortedByAngleFromPoint
from primitives import *
from rbTree import RedBlackTree
from visualizationPrimitives import Scene,LinesCollection,PointsCollection,createScene
from rayLineIntersection import detectIntersection

class VisibilityGraph:
    def __init__(self , obstaclePoints):
        '''obstaclePoints is a list of lists of points - each representing one obstacle'''
        obstacles = list()
        vertices = list()

        p_id=0
        for o_id , o in enumerate(obstaclePoints):
            newVertices = list()
            print("obstacle_id: " , o_id)
            for p in o:
                print("point_id: " , p_id , ", coords: " , p)
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

        # # Example of not working Tree
        # e1 = TreeEdge(vertices[0] , vertices[3] , vertices[4])
        # e2 = TreeEdge(vertices[0] , vertices[4] , vertices[5])
        # if e1 < e2:
        #     print("less")
        # if e2 < e1:
        #     print("more")

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
        return (G , E)

    def __visibleVerticesFrom(self , p0):
        EPS = 1e-10
        sortedPoints = sortedByAngleFromPoint(p0 , self.vertices , EPS)
        
        # debug or sth here
        print("sorted from " , p0.id , ": ")
        for p in sortedPoints:
            print(p.id ,"-> prev: ", p.prevP.id ,", next: " ,  p.nextP.id)
        print("")

        #initialize tree
        rbT = RedBlackTree()
        visibleVertices = []

        rayFrom = p0
        rayTo = sortedPoints[1]
        #add all edges that intersect the ray in its initial position [rayFrom , rayTo]
        for p in sortedPoints[1:]:
            intersectionPoint = detectIntersection([rayFrom.coords , rayTo.coords] , [p.coords , p.nextP.coords])
            if intersectionPoint != None:
                if epsEquals(intersectionPoint, p.coords, EPS) or epsEquals(intersectionPoint, p.nextP.coords, EPS):
                    pointOn = p
                    other = p.nextP
                    if epsEquals(intersectionPoint,p.nextP.coords,EPS):
                        #print("swap")
                        (other,pointOn) = (pointOn,other)

                    if ccw(rayFrom , pointOn , other) > EPS:
                        rbT.add(TreeEdge(rayFrom , p , p.nextP))
                else:
                    rbT.add(TreeEdge(rayFrom , p , p.nextP))
        
        self.scenes.append(createScene(rbT , [rayFrom,rayTo] , visibleVertices))

        #debug
        print("rbT:")
        for edge in list(rbT):
            print(edge.points)
        print("# # # #")

        #main loop
        previous = None
        for p in sortedPoints[1:]:
            if self.__visible(p0 , previous , visibleVertices , p , rbT):
                # print("visible: ",p, " from ", p0)
                visibleVertices.append(p)
            # else:
            #     print("invisible: ",p, " from ", p0)

            if ccw(p0 , p , p.nextP) > EPS:
                rbT.remove(TreeEdge(p0 , p , p.nextP))
            if ccw(p0 , p , p.prevP) > EPS:
                rbT.remove(TreeEdge(p0 , p , p.prevP))
            
            if ccw(p0, p, p.nextP) < -EPS:
                rbT.add(TreeEdge(p0, p, p.nextP))
            if ccw(p0, p, p.prevP) < -EPS:
                rbT.add(TreeEdge(p0, p, p.prevP))
            previous = p
            self.scenes.append(createScene(rbT , [rayFrom,rayTo] , visibleVertices))
        print("From: "+str(p0))
        for v in visibleVertices:
            print("v: "+str(v))
        return visibleVertices

    def __visible(self, p0, previous , visibleVertices, point , rbT):
        EPS = 1e-10
        """ checks if point is visible from p0 """
        if locallyIntersects(p0 , point , EPS):
            #print("F1")
            return False
        elif previous is None or abs(ccw(p0 , previous, point)) > EPS:
            e = rbT.findLeftmostValue()
            #print(e)
            if e is not None and e.points[0] != point and e.points[1] != point and cross(p0, point, e.points[0], e.points[1]):
                #print("F2")
                return False
            else:
                #print("T1")
                return True
        else:
            if len(visibleVertices)>0 and previous != visibleVertices[-1]:
                #print("F3")
                return False
            else:
                #print("__existsEdgeBetween: ", previous, point)
                return not __existsEdgeBetween(previous, point)
                #TODO search for edge intersecting [previous , point]

        def __existsEdgeBetween(nearPoint, farPoint, rbT):
            e1 = rbT.successor(TreeEdge(nearPoint.orientPoint, nearPoint, nearPoint.nextP))
            ek1 = TreeEdge(farPoint.orientPoint, farPoint, farPoint.nextP)
            ek2 = TreeEdge(farPoint.orientPoint, farPoint, farPoint.prevP)
            while e1 != None and e1 != ek1 and e1 != ek2:
                if cross(nearPoint, farPoint, e1.points[0], e1.points[1]):
                    return True
                e1 = rbT.successor(e1)
            return False