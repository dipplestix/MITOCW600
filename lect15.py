import math

class cartesianPoint(object):
    pass

cp1 = cartesianPoint()
cp2 = cartesianPoint()
cp1.x = 1.0
cp1.y = 2.0
cp2.x = 1.0
cp2.y = 3.0

def samePoint(p1, p2):
    return (p1.x == p2.x) and (p1.y == p2.y)
    
class cPoint(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.radius = math.sqrt(self.x**2+self.y**2)
        self.angle = math.atan2(self.y, self.x)
    def cartesian(self):
        return (self.x, self.y)
    def polar(self):
        return(self.radius, self.angle)
    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
    def __cmp__(self, other):
        return (self.x == other.x) and (self.y == other.y) 