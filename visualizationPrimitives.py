import matplotlib.collections as mcoll

def createScene(edgesOnTree , ray , visibleVertices):
    return Scene(points = [PointsCollection([v.coords for v in visibleVertices] , color = "green"),
                            PointsCollection([ray[0].coords] , color = "red" , s=100)],
                lines = [LinesCollection([e.pointCoords for e in edgesOnTree] , color = "orange"),
                        LinesCollection([[ray[0].coords , ray[1].coords]] , color = "red"),
                        LinesCollection([[ray[0].coords , v.coords] for v in visibleVertices] , color = "black")])

def createFinalScene(outputEdges):
    return Scene(lines = [LinesCollection([[e[0].coords, e[1].coords] for e in outputEdges] , color = "black")])

class Scene:
    def __init__(self, points=[], lines=[]):
        self.points=points
        self.lines=lines

class PointsCollection:
    def __init__(self, points, **kwargs):
        self.points = points
        self.kwargs = kwargs
    
    def add_points(self, points):
        self.points = self.points + points

class LinesCollection:
    def __init__(self, lines, **kwargs):
        self.lines = lines
        self.kwargs = kwargs
        
    def add(self, line):
        self.lines.append(line)
        
    def get_collection(self):
        return mcoll.LineCollection(self.lines, **self.kwargs)