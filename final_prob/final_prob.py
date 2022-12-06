import math

primes = []
a_primes = []

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
    for i in range(0, len(num)):
        total += int(num[i])
    return total

def prod_digits(num):
    num = str(num)
    total = 1
    for i in range(0, len(num)):
        total = total * int(num[i])
    return total

def is_am(num):
    dig_sum = sum_digits(num)
    dig_prod = prod_digits(num)
    return num + dig_sum + dig_prod

def is_a(num):
    dig_sum = sum_digits(num)
    return num + dig_sum

for i in range(len(primes)-1):
    if is_a(primes[i]) == primes[i+1]:
        a_primes.append(primes[i])

for i in range(len(primes)-1):
    if (is_am(primes[i]) == primes[i+1]) and primes[i] not in a_primes:
        print(primes[i])