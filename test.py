import math

k=24
n=k+23

n, k = 24 + 23, 24

print(math.factorial(n)//math.factorial(k)//math.factorial(n-k))

print(math.factorial(n) // math.factorial(k) // math.factorial(n-k))

def choose(n, k):
    return math.factorial(n) // math.factorial(k) // math.factorial(n-k)

b=23
print(choose(24 + b, 24)% 1000000007)
