#q3s1
from sympy.utilities.iterables import multiset_permutations
import numpy as np
a = np.array([1, 2, 3, 4, 5, 6])
record = 0
for p in multiset_permutations(a):
  #print(p)
  if (100*p[2]+50+p[3]) == 0.5*((10*p[0]+p[1])+(100*p[4]+40+p[5])):
    if (100*p[2]+50+p[3])*(10*p[0]+p[1])*(100*p[4]+40+p[5]) > record:
      record = (100*p[2]+50+p[3])*(10*p[0]+p[1])*(100*p[4]+40+p[5])

print(record)