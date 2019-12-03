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