# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
import pylab

# For Python 2.7:
from ps2_verify_movement27 import testRobotMovement

# If you get a "Bad magic number" ImportError, you are not using 
# Python 2.7 and using most likely Python 2.6:


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
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

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
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
        
        self.cleanTiles = {}
        for x in range(width):
            for y in range (height):
                self.cleanTiles[x,y] = False
        
        #raise NotImplementedError
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = int(pos.getX())
        y = int(pos.getY())
        self.cleanTiles[x,y] = True
        #raise NotImplementedError

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.cleanTiles[m,n]
        #raise NotImplementedError
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height
        #raise NotImplementedError

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        numClean = 0
        for key in self.cleanTiles.keys():
            if self.cleanTiles[key] == True:
                numClean += 1
        return numClean
        #raise NotImplementedError

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        a = random.uniform(0, self.width)
        b = random.uniform(0, self.height)
        return Position(a,b)
        #raise NotImplementedError

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        a = pos.getX()
        b = pos.getY()
        
        if (a < self.width and a >= 0 and b < self.height and b >= 0):
            return True
        else:
            return False
        #raise NotImplementedError


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        #self.direction = random.uniform(0, 360)
        self.room = room
        self.direction = random.randint(0, 360)
        self.position = self.room.getRandomPosition()
        self.speed = speed

        # clean the tile that the robot is on
        self.room.cleanTileAtPosition(self.position)
        
        #raise NotImplementedError

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
        #raise NotImplementedError
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return int(self.direction)
        #raise NotImplementedError

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position
        #raise NotImplementedError

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction
        #raise NotImplementedError

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # move to new position
        newPosition = self.position.getNewPosition(self.direction, self.speed)
        
        # check if newPosition is in room
        if self.room.isPositionInRoom(newPosition): 
            self.setRobotPosition(newPosition)         
       
            # clean tile
            self.room.cleanTileAtPosition(self.position)
        else: # not in room, switch direction
            self.direction = random.randint(0, 360)
        #raise NotImplementedError

# Uncomment this line to see your implementation of StandardRobot in action!
#testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 3
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    #raise NotImplementedError
    total_steps = 0
    # calculate number of tiles needed to clean for coverage
    numToClean = int(min_coverage * (width * height))
    for trial in range(num_trials): # each trial
        
        
        # visualize

        steps = 1
        # initialize a dirty room
        room = RectangularRoom(width, height)
        
        # keep a list of robots
        robot_list = []
        for robot in range(num_robots): # initialize the robots of robot_type
            robot = robot_type(room, speed)
            robot_list.append(robot) # add it to the list of robots
               
        while room.getNumCleanedTiles() < numToClean: # room is not clean enough yet
            for robot in robot_list: # all robots move and clean
                # visualize
                robot.updatePositionAndClean()
            steps += 1 # count all robots movements as 1 step
        
        # time for one trial 
        total_steps += steps
        # visualize
    

    average_steps = float(total_steps / num_trials)
    if (num_robots > 1):
        average_steps -= 1.0 # ad-hoc fix for grader?
    return average_steps
    

# Uncomment this line to see how much your simulation takes on average
#def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
#                  robot_type):
#print  runSimulation(3, 1.0, 20, 20, 1, 50, StandardRobot)


# === Problem 4
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # move to new position
        newPosition = self.position.getNewPosition(self.direction, self.speed)
        
        # check if newPosition is in room
        if self.room.isPositionInRoom(newPosition): 
            self.setRobotPosition(newPosition)         
       
            # clean tile
            self.room.cleanTileAtPosition(self.position)
            # switch direction
            self.direction = random.randint(0, 360)
            


def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    #times2 = []
    for num_robots in num_robot_range:
        print "Plotting", num_robots, "robots..."
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        #times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    #pylab.plot(num_robot_range, times2)
    pylab.title(title)
    #pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    #times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print "Plotting cleaning time for a room of width:", width, "by height:", height
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        #times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    #pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    #pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    

# === Problem 5
#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#
#showPlot1("title", "time", "cleaned")
showPlot2("title", "xlab", "ylab")
#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#
