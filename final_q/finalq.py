import math

def test_integer(a, b, c, n):
    return a**2 + b**2 + c**2 == n

def find_abc(n):
    out = []
    for a in range(int(math.sqrt(n))+1):
        for b in range(int(math.sqrt(n))+1):
            for c in range(int(math.sqrt(n))+1):
                if test_integer(a, b, c, n):
                    out.append([a, b, c])
    return out

print(len(find_abc(734)))
print(math.factorial(60))