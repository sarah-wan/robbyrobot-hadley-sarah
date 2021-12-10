import robby
import time
import random

test = []

POPULATION_SIZE = 100
GENOME_LENGTH = 243
MUTATION_RATE = 0.005
NUM_GENERATIONS = 100

TOTAL_MOVES = 200
CAN_DENSITY = 0.5
MOVE_DICTIONARY = {
    0: "MoveNorth", 
    1: "MoveSouth", 
    2: "MoveEast", 
    3: "MoveWest",
    4: "StayPut", 
    5: "PickUpCan", 
    6: "MoveRandom"
}
rw = robby.World(10, 10)

def generateGenomes():
    return [ ("".join(str(random.randint(0,6)) for i in range(GENOME_LENGTH))) for x in range(POPULATION_SIZE)]

def sortByFitness(genomes):
    tuples = [(calcFitness(g, TOTAL_MOVES), g) for g in genomes]
    tuples.sort()
    sortedFitnessValues = [f for (f, g) in tuples]
    sortedGenomes = [g for (f, g) in tuples]

    sumFit = sum(fit for fit, genome in tuples)
    avg = sumFit / POPULATION_SIZE

    return sortedGenomes, sortedFitnessValues, avg

def calcFitness(strategy, moves):
    score = 0
    # TODO: should we randomize where robot starts?
    rw.graphicsOff()
    rw.distributeCans(CAN_DENSITY)

    for i in range(moves):
        percept_code = rw.getPerceptCode()
        percept_string = rw.getPercept()

        move = int(strategy[percept_code])

        if (move == 6):
            move = random.randint(0,5)

        if (move <= 3 and percept_string[move] == 'W'):
            score -= 5

        if (move == 5 and percept_string[4] != 'C'):
            score -= 1
            
        if (move == 5 and percept_string[4] == 'C'):
            score += 10
        
        rw.performAction(MOVE_DICTIONARY[int(move)])

    return score

def mate(genome1, genome2):
    position = random.randint(0, GENOME_LENGTH-1)
    newGenome = genome1[0:GENOME_LENGTH] + genome2[GENOME_LENGTH:len(genome2)]

    for i in range(GENOME_LENGTH):
        if random.random() < MUTATION_RATE:
            newGenome = newGenome[:position] + str(random.randint(0,6)) + newGenome[position+1:]


    return newGenome

def main():
    population = generateGenomes()

    f = open("GAoutput6.txt", "a")
    sumRanks = POPULATION_SIZE * (POPULATION_SIZE + 1) / 2
    
    newpopulation = [''] * POPULATION_SIZE

    for i in range(NUM_GENERATIONS):
        [sortedGenomes, sortedFitnessValues, avg] = sortByFitness(population)
        if i % 10 == 0:
            rw.graphicsOn()
            test.append(sortedGenomes[random.randint(90,95)])
            f.write(str(i) + ": " + str(avg) + ", " + str(sortedFitnessValues[len(sortedFitnessValues) - 1]) + ", " + str(sortedGenomes[len(sortedGenomes) - 1]) + "\n")
        if i == (NUM_GENERATIONS - 1):
            f.write(str(i) + ": " + str(avg) + ", " + str(sortedFitnessValues[len(sortedFitnessValues) - 1]) + ", " + str(sortedGenomes[len(sortedGenomes) - 1]) + "\n")
            print(sortedGenomes)
            print(sortedFitnessValues)
        for i in range(POPULATION_SIZE):
            selected1 = random.randint(1, sumRanks)
            selected2 = random.randint(1, sumRanks)
            index1 = 0
            index2 = 0
            temp = sumRanks
            for j in range(POPULATION_SIZE):
                temp = temp - (POPULATION_SIZE - j)
                if index1 == 0 and selected1 > temp :
                    index1 = POPULATION_SIZE - j
                if index2 == 0 and selected2 > temp :
                    index2 = POPULATION_SIZE - j
            newpopulation[i] = mate(sortedGenomes[index1 - 1], sortedGenomes[index2 - 1])

        population = newpopulation


    f.close()
main()
print(test)
rw.graphicsOn()
for i in range(len(test) - 1):
    rw.demo(test[i])
    time.sleep(2)

# rw = robby.World(10, 10)

# stat = "656353656252353252656353656151353151252353252151353151656353656252353252656353656050353050252353252050353050151353151252353252151353151050353050252353252050353050656353562523532526563536561513531512523532521513531516563536562523532526563534543"
# rw.demo(stat, steps=200, init=0.50)


# print(calcFitness("65635365625235325265635365615135315125235325215135315165635365625235325265635365605035305025235325205035305015135315125235325215135315105035305025235325205035305065635356252353252656353656151353151252353252151353151656353656252353252656353454", TOTAL_MOVES))

# rw.demo(rw.strategyM)

# [x,y] = sortByFitness(generateGenomes())
# print(y)
