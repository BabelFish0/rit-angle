nums = [1, 2, 3, 4, 5, 6]
import math

def check(list):
    a = list[0]
    b = list[1]
    c = list[2]
    d = list[3]
    e = list[4]
    f = list[5]

    if round(((b/(c+1))*((2**(c+1))-(a**(c+1))) + e*(4-a**2), 4) == round((144*d)/f), 4): #and ((144*d) % f !=0):
        print(list)

def perm(a, k=0):
   if k == len(a):
        check(a)
        #print(a)
   else:
        for i in range(k, len(a)):
            a[k], a[i] = a[i] ,a[k]
            perm(a, k+1)
            a[k], a[i] = a[i], a[k]

perm(nums)