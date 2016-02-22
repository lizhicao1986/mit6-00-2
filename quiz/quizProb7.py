import random
import pylab

def LV():
    balls = ['white', 'black'] * 500
    random.shuffle(balls)    # shutffle the balls
    
    numTries = 0
    found = False
    while (not found):
        ball = random.choice(balls)
        numTries += 1
        if ball == 'white': # found it
            break
    return numTries

def MC(k):
    balls = ['white', 'black'] * 500
    random.shuffle(balls)    # shutffle the balls
    
    numTries = 0
    
    # random index
    index = random.randint(0, len(balls) -1)
    ball = balls[index]   
    numTries += 1

    
    if ball == 'white': # found it
        return 1
    else:
        # check if at end of list
        if index == (len(balls) - 1):
            index = 0 # loop back
            numTries += 1

        else:
            index +=1
            numTries += 1
            if balls[index] == 'white':
                return 2
    
    ### keep trying for k+2 more times
    while (numTries <= k - 2):
        if index == (len(balls) - 1):
            index = 0 # loop back
        else:
            index += 1
        numTries += 1
        if ball == 'white': # found it
            return numTries

    return 0 

histogram = [ 0 for i in range(1,1000)]  # intialize the list to be all zeros

for i in range(1000): # number of steps 

    result = LV() # number of tries

    histogram[ result ] += 1

pylab.plot(range(1, 20), histogram[1:20] )
pylab.show()

#####################333

histogram = [ 0 for i in range(1,1000)]  # intialize the list to be all zeros

for i in range(1000):

    result = MC(i)

    histogram[ result ] += 1

pylab.plot(range(1, 20), histogram[1:20] )
pylab.show()