from plot import Plot
"""
obstaclePoints = [[(1,1) , (3,4) , (1,5)] , [(4,2),(6,1),(7,4),(5,6)]]

my_plot = Plot()
my_plot.draw()

"""
from rbTree import *
from primitives import *

t1 = TreeEdge((0,0), (0,2), (1,0))
t2 = TreeEdge((0,0), (2,1), (2,-1))
t3 = TreeEdge((0,0), (2,2), (4,-2))

print(t1)
print(t2)
print(t3)

rbT = RedBlackTree()
rbT.add(t1)
rbT.add(t2)
rbT.add(t3)

print("Ans: ")
print(rbT.ceil(t1))
#print(rbT.ceil(t2))
#rbT.ceil(t3)