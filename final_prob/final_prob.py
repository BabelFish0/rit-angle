import math

primes = []

def is_prime(num):
    for div in range(2, int(math.sqrt(num))+1):
        if num % div == 0:
            return False
    return True

test_num = 2
while test_num <= 20000:
    if is_prime(test_num):
        primes.append(test_num)
    test_num += 1

#print(primes)

def sum_digits(num):
    num = str(num)
    total = 0
    for i in range(0, len(num)-1):
        total += int(num[i])
    return total



def is_am(num):
