# 6.00.2x Problem Set 4

import numpy
import random
import pylab
from ps3b import *




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
            numResistant = patient.getResistPop(resistances.keys())
            resistant_pop[step] = resistant_pop[step] +  numResistant
            
            
        patient.addPrescription('guttagonol')
        for step in range(150, 300): # 150 more time steps          
            virus_pop[step] += patient.update()
            #virus_pop[step] = virus_pop[step] + patient.getTotalPop() ##total virus pop at each time step
            numResistant = patient.getResistPop(resistances.keys())
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


#####################################

#        
def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    
    # TODO
    
    #virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) # initialize virus
    virus = ResistantVirus(0.1, 0.05, {'guttagonol':False}, 0.005) # initialize virus

    viruses = [virus] * 100 # 100 viruses
    maxPop = 1000   
    
    delays = [300, 150, 75, 0]
   # delays = [150]
    for delay in delays: # for each delay        
                 
        virus_pop = [0.0] * (delay + 150)
        #resistant_pop = [0.0] * (delay + 150)
        
        for trial in range(numTrials): # each trial
            
            patient = TreatedPatient(viruses, maxPop) # initialize patient
                    
    
            for step in range(delay): # time before adding drug (i.e. "Delay")          
                virus_pop[step] += patient.update()
                #virus_pop[step] = virus_pop[step] + patient.getTotalPop() ##total virus pop at each time step
                #numResistant = patient.getResistPop(resistances.keys())
                #resistant_pop[step] = resistant_pop[step] +  numResistant
                
                
            patient.addPrescription('guttagonol') # add drug
            for step in range(delay, delay + 150): # 150 more time steps          
                virus_pop[step] += patient.update()
                #virus_pop[step] = virus_pop[step] + patient.getTotalPop() ##total virus pop at each time step
                #numResistant = patient.getResistPop(resistances.keys())
                #resistant_pop[step] = resistant_pop[step] +  numResistant

        
        virus_pop_avg = []
        for item in virus_pop: # average virus pop at each time step
            #item = item / float(numTrials)
            virus_pop_avg.append(item/float(numTrials))
        
        #resistant_pop_avg = []
        #for item in resistant_pop: # average  pop at each time step
            #item = item / float(numTrials)
         #   resistant_pop_avg.append(item/float(numTrials))
            
        #plot histogram as frequency 
        virus_pop_avg = numpy.array(virus_pop_avg)
        #pylab.hist(virus_pop_avg, weights=numpy.zeros_like(virus_pop_avg) + 100./virus_pop_avg.size)    
        #pylab.hist(virus_pop_avg, bins=range(0, int(max(virus_pop_avg)+50), 10), weights=numpy.zeros_like(virus_pop_avg) + 100./virus_pop_avg.size)    
        pylab.hist(virus_pop_avg, bins=range(0, int(max(virus_pop_avg)+50), 10))    

    
        #print resistant_pop_plot
        #pylab.plot(range(delay + 150), virus_pop_avg, label='total virus')
        #pylab.plot(range(300), resistant_pop_plot, label='resistant virus') 
        #pylab.xlabel("time steps")
        #pylab.ylabel("# viruses")
        #pylab.legend()
        pylab.title("Delayed simulation" + str(delay))
        pylab.show()
        
#simulationDelayedTreatment(30)
#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    #virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) # initialize virus
    virus = ResistantVirus(0.1, 0.05, {'guttagonol':False, 'grimpex':False}, 0.005) # initialize virus

    viruses = [virus] * 100 # 100 viruses
    maxPop = 1000   
    
    delays = [300, 150, 75, 0] # delay before adding second drug
    #delays = [150]
    for delay in delays: # for each delay        
                 
        virus_pop = [0.0] * (delay + 300) #150 time steps before first drug, then delay, then 150 more times steps
            
        for trial in range(numTrials): # each trial
            patient = TreatedPatient(viruses, maxPop) # initialize patient
                    
            for step in range(150): # time before adding first drug           
                virus_pop[step] += patient.update()
                #virus_pop[step] = virus_pop[step] + patient.getTotalPop() ##total virus pop at each time step
                #numResistant = patient.getResistPop(resistances.keys())
                #resistant_pop[step] = resistant_pop[step] +  numResistant
                         
            patient.addPrescription('guttagonol') # add first drug
            
            for step in range(delay): # delay before adding second drug
                virus_pop[step] += patient.update()
                
            patient.addPrescription('grimpex') # add second drug

            for step in range(delay, delay + 150): # 150 more time steps          
                virus_pop[step] += patient.update()
                #virus_pop[step] = virus_pop[step] + patient.getTotalPop() ##total virus pop at each time step
                #numResistant = patient.getResistPop(resistances.keys())
                #resistant_pop[step] = resistant_pop[step] +  numResistant

        virus_pop_avg = []
        for item in virus_pop: # average virus pop at each time step
            #item = item / float(numTrials)
            virus_pop_avg.append(item/float(numTrials))
        

        #plot histogram as frequency 
        virus_pop_avg = numpy.array(virus_pop_avg)
        #pylab.hist(virus_pop_avg, weights=numpy.zeros_like(virus_pop_avg) + 100./virus_pop_avg.size)    
        pylab.hist(virus_pop_avg, bins=range(0, int(max(virus_pop_avg)+50), 50), weights=numpy.zeros_like(virus_pop_avg) + 100./virus_pop_avg.size)    
        #pylab.hist(virus_pop_avg, bins=range(0, int(max(virus_pop_avg)+50), 50))    

    
        #print resistant_pop_plot
        #pylab.plot(range(delay + 150), virus_pop_avg, label='total virus')
        #pylab.plot(range(300), resistant_pop_plot, label='resistant virus') 
        #pylab.xlabel("time steps")
        #pylab.ylabel("# viruses")
        #pylab.legend()
        pylab.title("Delayed simulation" + str(delay))
        pylab.show()
        print "variance of delay: " + str(delay) + " is " + str(numpy.var(virus_pop_avg))
    # TODO
    
simulationTwoDrugsDelayedTreatment(50)
