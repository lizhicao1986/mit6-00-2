import random

def oneOnNthRoll(n):
    # returns probability of one on this roll only!
    numTrials = 100000
    successes = [0] * numTrials

    for trial in range(numTrials):
        for roll in range(1, n+1): # roll dice    
            dice = random.choice(['1', '2', '3', '4', '5', '6'])
            if (dice == '1' and roll < n): # got a one before n
                successes[trial] = 0
                break
            elif (dice == '1' and roll == n): # got it on the nth roll, success
                successes[trial] = 1
                break

    
    # calculate probability (proprotion of ones in list)
    probability = 0.0
    totalCounts = 0
    for item in successes:
        totalCounts += item
    probability = float(totalCounts) / len(successes)
    return probability
  
    
def probTest(limit):
    
    numRolls = 100 # test 100 rolls
                    
    
    for roll in range(1, numRolls+1):
        # test each num of rolls
        probability = oneOnNthRoll(roll)
        if probability < limit: # met criteria, return roll
            return roll 
    # ran out of roll before limit
    return False
            
       
print probTest(0.1)        
print probTest(0.01) 
print probTest(0.05)
print probTest(0.005)
print probTest(0.001)
print probTest(0.0001)