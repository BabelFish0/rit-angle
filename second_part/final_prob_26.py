nums = [1, 2, 3, 4, 5, 6]
import math

import itertools
#print(list(itertools.permutations([1, 2, 3])))

def check(list):
    a = list[0]
    b = list[1]
    c = list[2]
    d = list[3]
    e = list[4]
    f = list[5]

    if (f*b)*((2**(c+1))-(a**(c+1))) + f*(c+1)*(40+2*e-((20*a**2+e*a**2)/2)) == ((c+1)*144*d):
    #if (b/(c+1))*((2**(c+1))-(a**(c+1))) + e*(4-a**2) == (144*d)/f:
        #if (f != 1 and ((144*d) % f == 0)) or f == 1:
        print(list)

for set in (list(itertools.permutations(nums))):
    check(set)

