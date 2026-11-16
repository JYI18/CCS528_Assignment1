import math

N = 15
a = 2

print("N =", N)
print("a =", a)

# GCD check
gcd_value = math.gcd(a, N)
print("gcd(a, N) =", gcd_value)

print("\nPowers of a mod N:")

for x in range(8):
    result = pow(a, x, N)
    print(f"{a}^{x} mod {N} = {result}")

# results period = 4
r = 4
print("\nPeriod r =", r)

# Extract factors
factor1 = math.gcd(pow(a, r // 2) - 1, N)
factor2 = math.gcd(pow(a, r // 2) + 1, N)

print("\nFactors:")
print(factor1)
print(factor2)