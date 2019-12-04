from plot import Plot
"""
obstaclePoints = [[(1,1) , (3,4) , (1,5)] , [(4,2),(6,1),(7,4),(5,6)]]

my_plot = Plot()
my_plot.draw()

"""
from rbTree import *
from primitives import *

p0 = Point([0,0], 0, 0)
p1 = Point([0,2], 1, 0)
p2 = Point([1,0], 2, 0)
p3 = Point([2,1], 3, 0)
p4 = Point([2,-1], 4, 0)
p5 = Point([2,2], 5, 0)
p6 = Point([4,-2], 6, 0)

t1 = TreeEdge(p0, p1, p2)
t2 = TreeEdge(p0, p3, p4)
t3 = TreeEdge(p0, p5, p6)

print(t1)
print(t2)
print(t3)

rbT = RedBlackTree()
rbT.add(t1)
rbT.add(t2)
rbT.add(t3)

print(t1 < t1)
print(t1 > t1)
print(t2 == t2)

print("Ans: ")
print(rbT.find_node(t1))
#print(rbT.ceil(t2))
#rbT.ceil(t3)