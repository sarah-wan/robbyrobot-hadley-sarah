import robby
import random

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

def calcFitness(strategy, moves):
    score = 0
    rw = robby.World(10, 10)
    # TODO: should we randomize where robot starts?
    rw.distributeCans(CAN_DENSITY)

    for i in range(moves):
        percept_code = rw.getPerceptCode()
        percept_string = rw.getPercept()

        move = strategy[percept_code]

        if (move == 6):
            move = random.randint(0,5)

        if (move <= 3 and percept_string[move] == 'W'):
            score -= 5

        if (move == 5 and percept_string[4] != 'C'):
            score -= 1
            
        if (move == 5 and percept_string[4] == 'C'):
            score += 10
        
        rw.performAction(MOVE_DICTIONARY[int(move)])

    return 0

print(calcFitness("656353656252353252656353656151353151252353252151353151656353656252353252656353656050353050252353252050353050151353151252353252151353151050353050252353252050353050656353656252353252656353656151353151252353252151353151656353656252353252656353454", TOTAL_MOVES))
