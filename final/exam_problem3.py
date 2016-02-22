import random
import pylab
from numpy import *

# Global Variables
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 500
CURRENTFOXPOP = 30

def rabbitGrowth():
    """ 
    rabbitGrowth is called once at the beginning of each time step.

    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.

    The global variable CURRENTRABBITPOP is modified by this procedure.

    For each rabbit, based on the probabilities in the problem set write-up, 
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP
    #global MAXRABBITPOP
    
    Prob_rab = 1.0 - CURRENTRABBITPOP/MAXRABBITPOP
    
    if random.random() < Prob_rab and CURRENTRABBITPOP < MAXRABBITPOP:
        CURRENTRABBITPOP +=1 
    
    # TO DO
    #pass
    
            
def foxGrowth():
    """ 
    foxGrowth is called once at the end of each time step.

    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.

    Each fox, based on the probabilities in the problem statement, may eat 
      one rabbit (but only if there are more than 10 rabbits).

    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.

    If it does not eat a rabbit, then with a 1/10 prob it dies.

    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP
    global CURRENTFOXPOP
    
    eaten_rab = False

    # TO DO
    Prob_fox_eats_rab = float(CURRENTRABBITPOP)/MAXRABBITPOP
    if CURRENTRABBITPOP > 10: # only if there are more than 10 rabbits
        if random.random() < Prob_fox_eats_rab:
            eaten_rab = True
            CURRENTRABBITPOP -= 1
    
    if eaten_rab: # 1/3 it gives birth to new fox
        if random.random() <= 0.3333333:
            CURRENTFOXPOP += 1
    
    if not eaten_rab:
        if random.random() <= 0.10 and CURRENTFOXPOP > 10:
            CURRENTFOXPOP -= 1
    
    
        
def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the 
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """
    rabbit_populations = []
    fox_populations = []
    
    for step in range(numSteps):
    # TO DO
        rabbitGrowth()
        foxGrowth()
        rabbit_populations.append(CURRENTRABBITPOP)
        fox_populations.append(CURRENTFOXPOP) 
    
    return (rabbit_populations, fox_populations)
    

result = runSimulation(200)
rabbitPopulationOverTime = result[0]
foxPopulationOverTime = result[1]

pylab.plot(range(len(rabbitPopulationOverTime)), rabbitPopulationOverTime)
pylab.title("rabbit")
pylab.show()

pylab.plot(range(len(foxPopulationOverTime)), foxPopulationOverTime)
pylab.title("fox")
pylab.show()

coeff = polyfit(range(len(rabbitPopulationOverTime)), rabbitPopulationOverTime, 2)

pylab.plot(polyval(coeff, range(len(rabbitPopulationOverTime))))
pylab.show()
 