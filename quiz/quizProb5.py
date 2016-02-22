import pylab
import random



def sampleQuizzes():
    numTrials = 10000
    
    
    
    range70_75 = [0] * 10000 # list to keep track of each trial
    
    for trial in range(numTrials): # determine if final grade is within range
        # determine midterm1 
        midterm1 = random.randint(50, 80)
        # determine midterm2
        midterm2 = random.randint(60, 90)

        # determine final exam
        finalExam = random.randint(55, 95)
        
        # compute final grade
        final_grade = 0.25*midterm1 + 0.25*midterm2 + 0.5*finalExam
        
        if (final_grade >= 70 and final_grade <= 75):
            range70_75[trial] = 1
        else:
            range70_75[trial] = 0
            
    
    # calculate probability (proprotion of ones in list)
    probability = 0.0
    totalCounts = 0
    for item in range70_75:
        totalCounts += item
    
    probability = float(totalCounts) / len(range70_75)
    return probability

def generateScores(numTrials):
    """
    Runs numTrials trials of score-generation for each of
    three exams (Midterm 1, Midterm 2, and Final Exam).
    Generates uniformly distributed scores for each of 
    the three exams, then calculates the final score and
    appends it to a list of scores.
    
    Returns: A list of numTrials scores.
    """
    
    scoresList = [None] * numTrials
    for trial in range(numTrials):
        # determine midterm1 
        midterm1 = random.randint(50, 80)
        # determine midterm2
        midterm2 = random.randint(60, 90)
        # determine final exam
        finalExam = random.randint(55, 95)
        # compute final grade
        final_grade = 0.25*midterm1 + 0.25*midterm2 + 0.5*finalExam
        scoresList[trial] = final_grade
    
    return scoresList
    
# plot histogram
def plotQuizzes():
    scoresList = generateScores(10000)
    pylab.hist(scoresList, bins=7)
    pylab.xlabel("Final Score")
    pylab.ylabel("Number of Trials")
    pylab.title("Distribution of Scores")
    pylab.show()

plotQuizzes()