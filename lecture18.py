from pylab import *
import random
#
#plot([1, 2, 3, 4])
#plot([5, 6, 7, 8])
#show()

vals = []
dieVals = [1,2,3,4,5,6]
for i in range(10000):
 vals.append(random.choice(dieVals)+random.choice(dieVals))
hist(vals, bins=11)
show() 