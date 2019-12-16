import matplotlib.pyplot as plt
import numpy as np
from visualizationPrimitives import LinesCollection, PointsCollection
from visibilityGraph import VisibilityGraph
import json as js

TOLERANCE = 0.05

def edgesToPoints(edges):
    return [e[0] for e in edges]

def pointsToEdges(points):
    n = len(points)
    return [(points[i], points[(i+1)%n]) for i in range(n)]

def dist(point1, point2):
    return np.sqrt(np.power(point1[0] - point2[0], 2) + np.power(point1[1] - point2[1], 2))

def diff(limits):
    return abs(limits[0] - limits[1])

class _Button_callback(object):
    def __init__(self, scenes):
        self.i = 0
        self.scenes = scenes
        self.adding_rects = False
        self.polygons_asLines = []
        self.polygons_asPoints = []
        self.json_file = "tests/test.json"

    def set_axes(self, ax):
        self.ax = ax
        
    def importFromJS(self, event):
        json = None
        with open(self.json_file, 'r') as file:
            json = file.read()
        self.polygons_asPoints = [PointsCollection(obstacle) for obstacle in js.loads(json)]
        self.polygons_asLines = [LinesCollection(pointsToEdges(polygon.points)) for polygon in self.polygons_asPoints]
        self.draw(autoscaling=True)

    def next(self, event):
        self.i = (self.i + 1) % len(self.scenes)
        self.draw(autoscaling = True)

    def prev(self, event):
        self.i = (self.i - 1) % len(self.scenes)
        self.draw(autoscaling = True)

    def add_rect(self, event):
        self.adding_rects = not self.adding_rects
        if self.adding_rects:
            self.new_rect()
    
    def run(self,event):
        vg = VisibilityGraph([edgesToPoints(rect.lines) for rect in self.polygons_asLines])
        vg.calculateVisibilityGraph()
        self.scenes.extend(vg.scenes)
    
    def new_rect(self):
        self.polygons_asLines.append(LinesCollection([]))
        self.polygons_asPoints.append(PointsCollection([]))
        self.newPolygonPoints = []
    
    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        new_point = (event.xdata, event.ydata)
        if self.adding_rects:
            if len(self.newPolygonPoints) == 0:
                self.newPolygonPoints.append(new_point)
            elif len(self.newPolygonPoints) > 2 and dist(self.newPolygonPoints[0], new_point) < (np.mean([diff(self.ax.get_xlim()), diff(self.ax.get_ylim())])*TOLERANCE):
                self.polygons_asLines[-1].add([self.newPolygonPoints[-1], self.newPolygonPoints[0]])
                self.polygons_asPoints[-1].points = self.newPolygonPoints
                self.new_rect()
            else:
                self.polygons_asLines[-1].add([self.newPolygonPoints[-1], new_point])
                self.newPolygonPoints.append(new_point)
            self.draw(autoscaling = False)
        
    def draw(self, autoscaling = True):
        if not autoscaling:
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
        self.ax.clear()
        for collection in self.polygons_asPoints:
            if len(collection.points) > 0:
                self.ax.fill(*zip(*(np.array(collection.points))), '0.7')
        for collection in (self.polygons_asLines + self.scenes[self.i].lines):
            self.ax.add_collection(collection.get_collection())
        for collection in (self.polygons_asPoints + self.scenes[self.i].points):
            if len(collection.points) > 0:
                self.ax.scatter(*zip(*(np.array(collection.points))), **collection.kwargs)
        self.ax.autoscale(autoscaling)
        if not autoscaling:
            self.ax.set_xlim(xlim)
            self.ax.set_ylim(ylim)
        plt.draw()