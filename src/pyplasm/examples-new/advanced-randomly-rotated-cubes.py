# Import libraries.
from pyplasm import *
from numpy import *
color = [220, 220, 220]

# Define 'n' random rotations.
def randRots(n):
    v = random.random_sample(4*n)
    return [ [2*PI*v[i],[v[i+1],v[i+2],v[i+3]]] for i in range(0,4*n,4) ]

# Number of cubes to intersect.
N = 100
  
# Intersect N randomly rotated cubes.
Cube = T(CUBE(2), -1, -1, -1)
rotations = AA(ROTN)(randRots(N))
out = TREE(COMP([JOIN, INTERSECTION]))(CONS(rotations)(Cube))

# View the result. The numbers between 0 and 1 
# are RGB components.
VIEW(COLOR(out, color))

