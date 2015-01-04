from math import * 

n = 100000
log_primes = log(2)

possible_primes = range(3, n, 2)

for i in possible_primes:
    for j in range(2, i//2):
        if i%j == 0:
            break
    else:
        log_primes += log(i)
        
print("The sum of the log of primes less than %d is %f. The ratio is %f" % 
    (n, log_primes, log_primes/n))
      