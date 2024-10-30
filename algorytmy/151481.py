import time
import sys
import random

def readTasks(filePath):
    with open(filePath, 'r') as file:
        lines = file.readlines()
    
    n = int(lines[0].strip())
    jobs = []
    for i in range(1, n + 1):
        p_j, d_j = map(int, lines[i].strip().split())
        jobs.append((p_j, d_j))
    
    transitions = []
    for i in range(n + 1, len(lines)):
        transitions.append(list(map(int, lines[i].strip().split())))
    
    return n, jobs, transitions

def saveResults(outputFile, order, delaySum):
    with open(outputFile, 'w') as file:
        file.write(str(delaySum) + "\n")
        file.write(" ".join(map(str, [job + 1 for job in order])) + "\n")

# delay
def calcLateness(currentTime, deadline):
    return max(0, currentTime - deadline)

def getTotalDelay(sequence, jobs, transitions):
    currentTime = 0
    totalLateness = 0
    for i, job in enumerate(sequence):
        p_j, d_j = jobs[job]
        if i > 0:
            prevJob = sequence[i - 1]
            currentTime += transitions[prevJob][job]
        currentTime += p_j
        totalLateness += calcLateness(currentTime, d_j)
    return totalLateness

# random
def createInitialOrder(n):
    order = list(range(n))
    random.shuffle(order)
    return order

def randomSwap(sequence, jobs, transitions, timeLimit, startTime):
    bestOrder = sequence[:]
    bestLateness = getTotalDelay(bestOrder, jobs, transitions)

    while time.time() - startTime < timeLimit:
        i, j = random.sample(range(len(sequence)), 2)
        
        newOrder = bestOrder[:]
        newOrder[i], newOrder[j] = newOrder[j], newOrder[i]
        
        newLateness = getTotalDelay(newOrder, jobs, transitions)
        
        if newLateness < bestLateness:
            bestOrder, bestLateness = newOrder, newLateness
        else:
            continue

    return bestOrder, bestLateness

def mainFunc(instFile, outFile, maxTime):
    startTime = time.time()
    n, jobs, transitions = readTasks(instFile)

    # limit czasu
    adjustedLimit = maxTime - 1

    order = createInitialOrder(n)

    bestOrder, bestLateness = randomSwap(order, jobs, transitions, adjustedLimit, startTime)
    
    print("Delay:", bestLateness)
    print("kolejność zadań:", " ".join(map(str, [job + 1 for job in bestOrder])))
    saveResults(outFile, bestOrder, bestLateness)
    print("Wyniki zapisane do", outFile, "Delay:", bestLateness)

    timeElapsed = time.time() - startTime
    if timeElapsed > adjustedLimit:
        print("przekroczono limit czasu:", round(timeElapsed, 2), "s")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("python algorytm instancje wynik czas")
        sys.exit("Brak wymaganych arg")
    
    instanceFile = sys.argv[1]
    outputFile = sys.argv[2]
    timeLimit = float(sys.argv[3])

    mainFunc(instanceFile, outputFile, timeLimit)
