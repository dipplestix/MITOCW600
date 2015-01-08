# Problem Set 11: Simulating robots
# Name:
# Collaborators:
# Time:
from pylab import *
import random, math
import ps11_visualize 

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real number indicating the y-coordinate
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


# === Problems 1 and 2

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.clean = {}
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        coord = (int(pos.getX()), int(pos.getY()))
        self.clean[coord] = 1
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        try: self.clean[(m, n)]
        except KeyError:
            return False
        else: 
            return True
            
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.height*self.width
    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.clean)
    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        randX = random.randint(0, self.width - 1)        
        randY = random.randint(0, self.height - 1)
        return Position(randX, randY)
    def isPositionInRoom(self, pos):
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """
        if pos.getX() < 0 or pos.getY() < 0:
            return False
        return pos.getX() <= self.width and pos.getY() <= self.height


class BaseRobot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in
    the room.  The robot also has a fixed speed.

    Subclasses of BaseRobot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified
        room. The robot initially has a random direction d and a
        random position p in the room.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the robot's position.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.speed = speed
        self.room = room
        self.d = random.randint(0, 360)
        self.p = self.room.getRandomPosition()
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.p
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.d
    def getRobotSpeed(self):
        return self.speed
    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.p = position
    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.d = direction


class Robot(BaseRobot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        p_0 = self.getRobotPosition()
        p_1 = p_0.getNewPosition(self.getRobotDirection(), self.speed)
        if self.room.isPositionInRoom(p_1):
            self.setRobotPosition(p_1)
            self.room.cleanTileAtPosition(p_1)
        else:
            self.setRobotDirection(random.randint(0, 360))
            
# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the room that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the room is clean.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE,
    each with speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: a boolean (True to turn on visualization)
    """
    coverageResults = []
    for t in range(num_trials):
        if visualize: anim = ps11_visualize.RobotVisualization(num_robots, width, height)
        #Create the room
        loopRoom = RectangularRoom(width, height)
        #create a list of robots using the new room and speed provided
        robots = []
        for r in range(num_robots):
            robots.append(robot_type(loopRoom, speed))
        #Clean the room
        clean = [0]
        while percentCoverage(loopRoom) < min_coverage:
            if visualize:anim.update(loopRoom, robots) 
            for robot in robots:
                robot.updatePositionAndClean()
            clean.append(percentCoverage(loopRoom))
        if visualize:anim.done() 
        coverageResults.append(clean)
    return coverageResults
        
def percentCoverage(room):
    return room.getNumCleanedTiles() / room.getNumTiles()

        

# === Provided function
def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = pylab.array(tots)
    # Compute means
    means = tots/float(len(list_of_lists))
    return means


# === Problem 4
def meanTime(list_of_lists):
    lengths = []
    for lists in list_of_lists:
        lengths.append(len(lists))
    return sum(lengths)/len(lengths)

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    sizes = [5, 10, 15, 20, 25]
    numsim = 100
    result = []
    for size in sizes:
        a = runSimulation(1, 1, size, size, .75, numsim, Robot, False)
        result.append(meanTime(a))
    figure()
    plot(sizes, result)
    xlabel('Room Size')
    ylabel('Amount of time')
    title('Size of a room vs amount of time taken to clean it')

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    numsim = 100
    result = []
    for robots in range(1, 11):
        a = runSimulation(robots, 1, 25, 25, .75, numsim, Robot, False)
        result.append(meanTime(a))
    figure()
    plot(list(range(1,11)), result)
    xlabel('# of Robots')
    ylabel('Amount of time')
    title('Number of Robots vs amount of time taken to clean 25x25 Room')
        

def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    l = [20, 25, 40, 50, 80, 100]
    numsim = 1000
    result = []
    for length in l:
        a = runSimulation(2, 1, length, 400/length, .75, numsim, Robot, False)
        result.append(meanTime(a))
    figure()
    plot(l, result)
    xlabel('Width of Room')
    ylabel('Amount of time')
    title('Width of Room vs amount of time taken to clean 25x25 Room')

#def showPlot4():
#    """
#    Produces a plot showing cleaning time vs. percentage cleaned, for
#    each of 1-5 robots.
#    """
#    numsim = 100
#    results = []
#    cloverageps = array((range(0, 105, 5)))/100
#    for robots in range(1, 6):
#        print(robots)
#        result = []
#        for clean in coverageps:
#            a = runSimulation(robots, 1, 25, 25, clean, numsim, Robot, False)
#            result.append(meanTime(a))
#        results.append(result)
#    a = computeMeans(results)


# === Problem 5

class RandomWalkRobot(BaseRobot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """
    # TODO: Your code goes here
    def updatePositionAndClean(self):
        p_0 = self.getRobotPosition()
        self.setRobotDirection(random.randint(0, 360))
        p_1 = p_0.getNewPosition(self.getRobotDirection(), self.speed)
        if self.room.isPositionInRoom(p_1):
            self.setRobotPosition(p_1)
            self.room.cleanTileAtPosition(p_1)

# === Problem 6

def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    """
    # TODO: Your code goes here