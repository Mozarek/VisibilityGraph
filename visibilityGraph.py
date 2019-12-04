import numpy as np
from sortUtil import sortedByAngleFromPoint
from primitives import *
from rbTree import *
from visualizationPrimitives import Scene,LinesCollection,PointsCollection

class VisibilityGraph:
    def __init__(self , obstaclePoints):
        '''obstaclePoints is a list of lists of points - each representing one obstacle'''
        obstacles = list()
        vertices = list()

        p_id=0
        for o_id , o in enumerate(obstaclePoints):
            print("obstacle_id: " , o_id)
            for p in o:
                print("point_id: " , p_id , ", coords: " , p)
                vertices.append(Point(p,p_id,o))
                p_id+=1
            obstacles.append(Obstacle(vertices[-len(o):] ,o_id))
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

        return (G , E)

    def __visibleVerticesFrom(self , point):
        def __visible(self, visiblePoint):
            leftmostEdge = 
            return False
        sortedPoints = sortedByAngleFromPoint(point , self.vertices , 1e-10)
        """ debug or sth here
        print("sorted from " , point.id , ": ")
        for p in sortedPoints:
            print(p.id , end=' ')
        print("")
        """
        #magic check begins
        rbT = RedBlackTree()
        visible = list()
        #TODO: use magic to check which of sortedPoints are visible from point
        return sortedPoints


        