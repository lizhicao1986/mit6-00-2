# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import numpy
import random
import pylab
#from ps3b_precompiled_27 import *   
''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        # TODO
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        # TODO
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """

        # TODO
        if self.getClearProb() >= random.random():
            return True
        else:
            return False


    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        # TODO
        probReproduce = self.getMaxBirthProb() * (1 - popDensity)
        if probReproduce > random.random():
            offspring = SimpleVirus(self.getMaxBirthProb(), self.getClearProb())
            return offspring
        else:
            raise NoChildException



class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        # TODO
        self.viruses = viruses
        self.maxPop = maxPop
        

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        # TODO
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        # TODO
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        # TODO       
        total = 0
        for virus in self.getViruses(): 
            total += 1
        return total

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        viruses_survived = []
        for virus in self.getViruses(): # check for survial
            if virus.getClearProb() < random.random(): # didn't get cleared, survives
                viruses_survived.append(virus)
                
        #re-initialize virus list
        self.viruses = viruses_survived
        
        #print "Number of viruses: ", len(self.viruses)
        
        # population density: current virus population divided by the maximum population.
        popDensity = len(self.viruses) / float(self.getMaxPop())
        
        for virus in self.getViruses():
            try:
                newVirus = virus.reproduce(popDensity)
                self.viruses.append(newVirus)
            except NoChildException as error:
                pass
                #print "No virus reproduced"
        
        return self.getTotalPop()



##### testing

#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """    
    virus = SimpleVirus(maxBirthProb, clearProb) # initialize virus
    #patient = Patient([virus]*numViruses, maxPop) # initialize patient
    
    for trial in range(numTrials): # each trial
        #virus_pop = []
        patient = Patient([virus]*numViruses, maxPop) # initialize patient
        virus_pop = [0.0] * 300
        for step in range(300): # 300 time steps          
            totalPop = patient.update()
            virus_pop[step] = virus_pop[step] + patient.getTotalPop() ##total virus pop at each time step
        #pylab.plot(range(300), virus_pop)
        #pylab.show()
    
    #virus_pop = numpy.divide(virus_pop, float(numTrials)) # average virus pop at each time step
    
    for item in virus_pop: # average virus pop at each time step
        item = item / float(numTrials)
    
    pylab.plot(range(300), virus_pop)
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend()
    pylab.title("SimpleVirus simulation")
    pylab.show()
    

    # TODO
    
    
    
    

#
# PROBLEM 4
#


class ResistantVirus(SimpleVirus):


    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):


        # TODO
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        #super(ResistantVirus, self).__init__(maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):

        # TODO
        return self.resistances

    def getMutProb(self):

        # TODO
        return self.mutProb

    def isResistantTo(self, drug):

        
        #for key in self.getResistances().keys():
        #    if key == drug:
        #        if self.getResistances()[drug] == True:
        #            return True
        #return False
        if drug in self.getResistances().keys(): # drug is in list of drugs
            return self.getResistances()[drug]
        else: # not in list, not resistant
            return False
        # TODO


    def reproduce(self, popDensity, activeDrugs):

        # TODO
        # determine drug resistance(s)
        probReproduce = self.getMaxBirthProb() * (1-popDensity) 
        for drug in activeDrugs:
            if self.isResistantTo(drug) == False: # not drug resistant, cannot reprod
                probReproduce = 0.0
                #break
        
        if probReproduce > random.random(): # reproduce
            parent_resistances = self.getResistances()
            mutProb = self.getMutProb()

            child_resistances = {}
            #determine if resistance is passed on
            for key in parent_resistances.keys():

                    
                if (1 - mutProb) > random.random(): # inherit resistance
                        child_resistances[key] = parent_resistances[key]
                else: # loses resistance
                        child_resistances[key] = not parent_resistances[key]
                    
            offspring =  ResistantVirus(self.getMaxBirthProb(), self.getClearProb(), child_resistances, mutProb)
            return offspring
        else:
            raise NoChildException


class TreatedPatient(Patient):


    def __init__(self, viruses, maxPop):
 

        # TODO
        #super(TreatedPatient, self).__init__(viruses, maxPop)
        Patient.__init__(self, viruses, maxPop)
        self.treatmentDrugs = []



    def addPrescription(self, newDrug):
       
   #     Administer a drug to this patient. After a prescription is added, the
    #    drug acts on the virus population for all subsequent time steps. If the
    #    newDrug is already prescribed to this patient, the method has no effect.

     #   newDrug: The name of the drug to administer to the patient (a string).

      #  postcondition: The list of drugs being administered to a patient is updated
    

        # TODO
        if newDrug in self.getPrescriptions(): # already in the list
            pass
        else: # new drug
            self.treatmentDrugs.append(newDrug)


    def getPrescriptions(self):


        # TODO
        return self.treatmentDrugs


    def getResistPop(self, drugResist):


        
        # check if drugResist list is empty, if so, return 0 (no drug resistant virus)
        if not drugResist:
            return 0
        else:
        
            resistantPop = 0
            allResist = False # assume no initial drug resistant
            
            for virus in self.getViruses(): # all viruses in patient
                allResist = False # assume no initial drug resistant
                
                for drug in drugResist: # each drug on list
                    if virus.isResistantTo(drug) == False:
                        allResist = False
                        break
                    else: 
                        allResist = True
                
                if (allResist): # virus is pan-resistant
                    resistantPop += 1
            return resistantPop

    def update(self):

        #print "in patient.update()"
        # TODO
        
        viruses_survived = []
        for virus in self.getViruses(): # check for survial
            if virus.getClearProb() < random.random(): # didn't get cleared, survives
                viruses_survived.append(virus)
                
        #re-initialize virus list
        self.viruses = viruses_survived
                
        # population density: current virus population divided by the maximum population.
        popDensity = self.getTotalPop() / float(self.getMaxPop())
        
        activeDrugs = self.getPrescriptions() # list of drugs the patient is on
        
        ## loop over virus list to reproduce
        newVirusList = self.getViruses()[:] # copy of virus list

        for virus in self.getViruses():
            try:
                newVirus = virus.reproduce(popDensity, activeDrugs)
                #self.viruses.append(newVirus)
                newVirusList.append(newVirus)
                #print "new virus produced"
            except NoChildException as error:
                pass
                #print "No virus reproduced"
        
        #re-initialize virus list
        self.viruses = newVirusList
        return self.getTotalPop()



###

#virus = ResistantVirus(0.1, 0.05, {'guttagonol':False}, 0.1)
#patient = TreatedPatient([virus]*100, 1000)
#patient.addPrescription('drug3')
#totalPop = 0
#for i in range(10): # 100 steps
    #totalPop = patient.update()
 #   patient.update()
  #  print "Total virus " , patient.getTotalPop()
   # print "Resistant to drug: ", patient.getResistPop(['guttagonol'])
   
    
#patient.addPrescription('drug3')
#print "adding drug--->>>>>>>>>>>>>"
#for i in range(10): # 100 steps
    #print patient.update()
 #   patient.update()
  #  print "Total virus " , patient.getTotalPop()
  #  print "Resistant to drug: ", patient.getResistPop(['guttagonol'])

#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """

    # TODO
    virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) # initialize virus
    #patient = Patient([virus]*numViruses, maxPop) # initialize patient
    
    virus_pop = [0.0] * 300
    resistant_pop = [0.0] * 300
    
    for trial in range(numTrials): # each trial
        #virus_pop = []
        patient = TreatedPatient([virus]*numViruses, maxPop) # initialize patient
                

        for step in range(150): # 150 time steps          
            virus_pop[step] += patient.update()
            #virus_pop[step] = virus_pop[step] + patient.getTotalPop() ##total virus pop at each time step
            #numResistant = patient.getResistPop(resistances.keys())
            numResistant = patient.getResistPop(['guttagonol'])
            if (numResistant == 0):
                resistant_pop[step] = 0
            else:
                resistant_pop[step] = resistant_pop[step] +  numResistant
            #resistant_pop[step] = resistant_pop[step] +  numResistant
            
            
        patient.addPrescription('guttagonol')
        for step in range(150, 300): # 150 more time steps          
            virus_pop[step] += patient.update()
            #virus_pop[step] = virus_pop[step] + patient.getTotalPop() ##total virus pop at each time step
            #numResistant = patient.getResistPop(resistances.keys())
            numResistant = patient.getResistPop(['guttagonol'])
            if (numResistant == 0):
                resistant_pop[step] = 0
            else:
                resistant_pop[step] = resistant_pop[step] +  numResistant

    
    virus_pop_plot = []
    for item in virus_pop: # average virus pop at each time step
        #item = item / float(numTrials)
        virus_pop_plot.append(item/float(numTrials))
    
    resistant_pop_plot = []
    for item in resistant_pop: # average  pop at each time step
        #item = item / float(numTrials)
        resistant_pop_plot.append(item/float(numTrials))
        
    print resistant_pop_plot
    pylab.plot(range(300), virus_pop_plot, label='total virus')
    pylab.plot(range(300), resistant_pop_plot, label='resistant virus') 
    pylab.xlabel("time steps")
    pylab.ylabel("# viruses")
    pylab.legend()
    pylab.title("ResistantVirus simulation")
    pylab.show()
    
    
random.seed(0)
#simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5)
simulationWithDrug(100, 1000, 0.1, 0.05, {'guttagonol':False}, 0.005, 10)

simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5)
#simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5)