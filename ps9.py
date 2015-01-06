# 6.00 Problem Set 9
#
# Name:
# Collaborators:
# Time:

from string import *
import copy

class Shape(object):
    def area(self):
        raise AttributeException("Subclasses should override this method.")

class Square(Shape):
    def __init__(self, h):
        """
        h: length of side of the square
        """
        self.side = float(h)
    def area(self):
        """
        Returns area of the square
        """
        return self.side**2
    def __str__(self):
        return 'Square with side ' + str(self.side)
    def __eq__(self, other):
        """
        Two squares are equal if they have the same dimension.
        other: object to check for equality
        """
        return type(other) == Square and self.side == other.side
    def __lt__(self, other):
        return str(self) < str(other)

class Circle(Shape):
    def __init__(self, radius):
        """
        radius: radius of the circle
        """
        self.radius = float(radius)
    def area(self):
        """
        Returns approximate area of the circle
        """
        return 3.14159*(self.radius**2)
    def __str__(self):
        return 'Circle with radius ' + str(self.radius)
    def __eq__(self, other):
        """
        Two circles are equal if they have the same radius.
        other: object to check for equality
        """
        return type(other) == Circle and self.radius == other.radius
    def __lt__(self, other):
        return str(self) < str(other)


#
# Problem 1: Create the Triangle class
#
## TO DO: Implement the `Triangle` class, which also extends `Shape`.
class Triangle(Shape):
    def __init__(self, base, height):
        self.base = float(base)
        self.height = float(height)
    def area(self):
        '''Returns the area of a triangle '''
        return .5*self.base*self.height
    def __str__(self):
        return 'Triangle with base %.1f and height %.1f' % (self.base, self.height)
    def __eq__(self, other):
        return type(other) == Triangle and self.base == other.base and self.height == other.height
    def __lt__(self, other):
        return str(self) < str(other)

#
# Problem 2: Create the ShapeSet class
#
## TO DO: Fill in the following code skeleton according to the
##    specifications.

class ShapeSet:
    def __init__(self):
        """
        Initialize any needed variables
        """
        self.shapes = []
    def addShape(self, sh):
        """
        Add shape sh to the set; no two shapes in the set may be
        identical
        sh: shape to be added
        """
        if not sh in self.shapes:
            self.shapes.append(sh)
        else:
            print('Already in the set')
            
    def __iter__(self):
        """
        Return an iterator that allows you to iterate over the set of
        shapes, one shape at a time
        """
        self.index = 0
        return self
    def __next__(self):
        if self.index >= len(self.shapes):
            raise StopIteration
        self.index += 1
        return self.shapes[self.index-1]
    def __str__(self):
        """
        Return the string representation for a set, which consists of
        the string representation of each shape, categorized by type
        (circles, then squares, then triangles)
        """
        res = ''
        sortedshapes = copy.copy(self.shapes)
        sortedshapes.sort()
        for shape in sortedshapes:
            res += "{0}\n".format(shape)
        return res

#
# Problem 3: Find the largest shapes in a ShapeSet
#
def findLargest(shapes):
    """
    Returns a tuple containing the elements of ShapeSet with the
       largest area.
    shapes: ShapeSet
    """
    largest = (0,) 
    for shape in shapes:
        try:
            if shape.area() > largest[-1].area():
                largest = (shape, )
            elif shape.area() == largest[-1].area():
                largest += (shape, )
        except AttributeError:
            largest = (shape, )
    return largest
        
    

#
# Problem 4: Read shapes from a file into a ShapeSet
#
def readShapesFromFile(filename):
    """
    Retrieves shape information from the given file.
    Creates and returns a ShapeSet with the shapes found.
    filename: string
    """
    shapes = open(filename)
    shapeset = ShapeSet()
    for lines in shapes:
        shape = lines.strip().split(',')
        loopshape = shape[0][0].upper()+shape[0][1:]
        shapeclass = globals()[loopshape]
        if len(shape) > 2:
            shapeset.addShape(shapeclass(shape[1], shape[2]))
        else:
            shapeset.addShape(shapeclass(shape[1]))
    return shapeset