import matplotlib.collections as mcoll

def createScene(edgesOnTree , ray , visibleVertices):
<<<<<<< HEAD
    print([v.coords for v in visibleVertices])
    print(ray[0])
=======
    print("          CS_visible: " + str([v.coords for v in visibleVertices]))
    print("          CS_ray: " + str(ray))
>>>>>>> e5dbb82def7b69f8d2a735356c4ddf9ff77bfd1b
    return Scene(points = [PointsCollection([v.coords for v in visibleVertices] , color = "green"),
                            PointsCollection([ray[0].coords] , color = "red" , s=100)],
                lines = [LinesCollection([e.pointCoords for e in edgesOnTree] , color = "orange"),
                        LinesCollection([[ray[0].coords , ray[1].coords]] , color = "red")])

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