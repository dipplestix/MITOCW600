prime_count = 1 #2 is prime
how_many = 1000

possible_primes = range(3, 10000000000, 2)

for i in possible_primes:
    for j in range(2, i//2):
        if i%j == 0:
            break
    else:
        prime_count += 1
        if prime_count == how_many:
            print(i)
            break
