#Anirudh Satish
#Adam Beckwith
#Aldrin Feliciano

#Picobot genetic project
# 13th december 2019


#Picobot represented as O and spaces that have been covered represented by H


import random


SURROUNDINGS =  ["xxxx", "Nxxx", "NExx", "NxWx", "xxxS", "xExS", "xxWS", "xExx", "xxWx" ]
 
NUMSTATES = 5
HEIGHT = 25
WIDTH = 25 



class Program(object):
    ''' A class designed to show and implement code that works and looks like the code in Picobot.
    This does not take an input, and code can only be created via randomize(). The representation 
    also matches picobot. The code is stored as a dictionary, key is a touble with the initial state 
    and surroundings, while the  
    '''
    def __init__(self):
        """constructor """
        self.rules = {} 
        

    def __repr__(self):
        """representation of the dictionary. outputs a string of rules for picobot"""
        unsorted = list(self.rules.keys())          #unsorted list of keys
        sortedL = sorted(unsorted)                  #sorted list of keys 

        s = ""
        for i in range(len(sortedL)):               #loop to represent
            s = s + str(sortedL[i][0]) + " " + sortedL[i][1] + " -> " + self.rules[sortedL[i]][0] + " " + str(self.rules[sortedL[i]][1]) + "\n"
            
        return s 
    
    def randomize(self):
        """ generates a random, full set of rules for the program's self.rules dictionary
        which is a data member of the program class.  There are 5 states and 9 surroundings,
        so there ends up being 45 randomly-generated rules."""

        POSSMOVES = ["N", "W", "E", "S", "X"]                   #list of possible moves at each single position 
        ourlist = ["xxxx", "Nxxx", "NExx", "NxWx", "xxxS", "xExS", "xxWS", "xExx", "xxWx" ]        #list of all possible surroudings 
        for i in range(NUMSTATES):                              
            for surr in ourlist:
                movedir = random.choice(POSSMOVES)              #random move generated
                while movedir in surr:                          #if move is invalid, runs until it is valid 
                    movedir = random.choice(POSSMOVES)

                ourtuple = (movedir, random.choice(range(NUMSTATES)))
                self.rules[(i, surr)] = ourtuple 
        

    def getMove(self, state, surroundings):
        ''' returns the next move direction and new state change touple, from the key (state, surroundings)
        '''
        return self.rules[(state, surroundings)]
            
    def mutate(self):
        ''' Picks a random line of the picobot code, and changes the new move and the new state portions to
        a new random version. Initial state and surruoundings stay unchanged. Represents a small mutation  
        '''
        listK = list(self.rules.keys())         #list of keys of the rules dictionary
        randomkey = random.choice(listK)
        
        POSSMOVES = ["N", "W", "E", "S", "X"]

        movedir = random.choice(POSSMOVES)
        while movedir in randomkey[1]:             #random move generated
            movedir = random.choice(POSSMOVES)                          #if move is invalid, runs until it is valid 

        randomstate = random.choice(range(NUMSTATES))       #Generates random state 
        newelement = (movedir, randomstate)
        
        self.rules[randomkey] = newelement                  #changes the element of that particular key in self.rules
        
    
    def crossover(self, other):
        ''' Takes another Program list and combines them to create a "child" of the two, and returns the 
        child. It takes the initial states from 0-X from one parent, the rest from the other. Where x is a random 
        number from 0 to NUMSTATES 
        '''
        crossstate = random.choice(range(NUMSTATES))                #random cross over state generated 
        
        newprogram = Program()

        for i in range(crossstate + 1):                         #parent 1
            for j in SURROUNDINGS:
                newprogram.rules[(i , j)] = self.rules[( i, j)]

        for i in range(crossstate + 1, NUMSTATES):              #parent 2
            for j in SURROUNDINGS:
                newprogram.rules[(i, j)] = other.rules[( i, j)]

        return newprogram 

    def __gt__(self, other):
        """Greater-than operator -- works randomly, but works!"""
        return random.choice([True, False])

    def __lt__(self, other):
        """Less-than operator -- works randomly, but works!"""
        return random.choice([True, False])

    def __eq__(self, other):
        ''' Checks if all the data and code are exactly the same between 21 programs 
        '''
        return self.rules == other.rules 

class World(object):
    ''' An Class designed to represent a changeing picobot board. it "Remembers"
     Picobot location and locations the picobot has already been. Takes picobot initial row, column
     and the program of class Program to run.  
    '''
    def __init__(self,initialrow,initialcol,program):
        ''' Constructor, holds data for everything. 
        '''
        self.row = initialrow
        self.col = initialcol
        self.state = 0
        self.prog = program 
        self.room = [[" "]*WIDTH for row in range(HEIGHT)]
        #Adding the walls. 
        for x in range(1,HEIGHT-1):
            self.room[x][0] = "|"
            self.room[x][-1] = "|"
        self.room[0] = ["="]*WIDTH
        self.room[-1] = ["="]*WIDTH
        
    
    def __repr__(self): 
        """Representation funciton to represent the objects of this class.
        it Displays the current board, with picobot, the spaces it has already
        traversed and the walls/boundaries of the board"""
        s = ""
        
        for row in range(HEIGHT): 
           
            for col in range(WIDTH):
                if row == self.row and col == self.col:                    
                    s+= "O"                                              #picobot!
                else:
                    s+= self.room[row][col]         
            s+= "\n"
        
        return s
    
    def getCurrentSurroundings(self):
        """Gets the current surroundings of picobot in the NEWS format, with x indicating
        no wall in that direction"""

        row = self.row 
        col = self.col 
        s = ""
        data = self.room 
        #set of 4 if conditions to check for the surroundings 
        if data[row-1][col] == "=": 
            s += "N"
        else:
            s+= "x"
        if data[row][col+1] == "|":
            s += "E"
        else:
            s+= "x"
        if data[row][col-1] == "|":
            s += "W"
        else:
            s+= "x"
        if data[row+1][col] == "=":
            s += "S"
        else:
            s+= "x"
        return s 

    def step(self):
        """makes the next move for picobot. Uses the getMove function from 
        Program class, generating the move from a randomly generated dictionary of 
        moves. Uses the curretnsurroundings as the key to access the next move in the
        dictionary"""

        nowsurr = self.getCurrentSurroundings()     #current surroundings

        program = self.prog                         #program
        nextmove = program.getMove(self.state, nowsurr)         #gets the next move 

        newdir, newstate = nextmove                     
        self.room[self.row][self.col] = "H"         #visited cells 

        #set of 4 if statements for each possible new move direction 
        if newdir == "N":
            self.row -= 1
        elif newdir == "E":
            self.col += 1
        elif newdir == "W":
            self.col -= 1
        elif newdir == "S":
            self.row += 1

        self.state = newstate


    def run(self, steps):
        """loops over the step function, executing it "step" number of times"""
        
        for i in range(steps):      #calls step as many times as required by step parameter    
            self.step()

    def fractionVisitedCells(self):
        '''Looks at the data stored on the board, and finds the fractional percentage of 
        "visited cells" vrs total amount of possible locations to be (not walls) 
        '''
        count = 0

        for row in range(HEIGHT):       #to count the number of cells visited 
            for col in range(WIDTH):
                if self.room[row][col] == "H":
                    count += 1 
        #since picobot isnt in the list representation of the board, rather stored as 2 values of row and col and hovers over the board
        #we use this condition to check if picobot is already on a space that has been covered 
        if self.room[self.row][self.col] != "H":
            count += 1
        
        denominator = (WIDTH - 2)*(HEIGHT - 2)
        return count/denominator


def genPop(n):
    """Creates n number of random picobot programs
    returns it as a list """

    ourlist = []
    for i in range(n):
        ourprog = Program()
        ourprog.randomize()

        ourlist += [ourprog]
    
    return ourlist 

def evaluateFitness(program, trials, steps):
    '''Takes a program and runs it "trials" times, and averages the fraction of visited cells 
    over those trials. Each trial has a random starting point. Each trial is run with "steps" number of 
    steps before concluding. 
    '''
    fitsum = 0.0
    for i in range(trials):         #counting total fitness over all trials 
        startrow = random.choice(range(1,HEIGHT - 1))
        startcol = random.choice(range(1,WIDTH - 1))

        w = World(startrow, startcol, program)
        w.run(steps)
        fitsum += w.fractionVisitedCells()

    return fitsum/trials        #average fitness 


def GA(popsize, numgens):
    '''Runs a genetic algaryth with a population of popsize and numgens generations. Every generation 
    takes the top (10) percent and crosses them, (mutatating every 3 child) and creates a new population of 
    popsize with 90% child and 10% the parents. prints data on each generation returns the best program.   
    '''
    trials = 50
    steps = 1000
    generations = genPop(popsize)       #list of programs of picobot 
    LC = [(evaluateFitness(generations[i], trials, steps), generations[i]) for i in range(popsize)]     #making a list of tuples with fitness and program 
        
    ourlist = sorted(LC) #sorting in ascending order of fitnesss

    #printing the current fitnesses for generation 0/ before the first parents cross 
    print("Generations: 0" )
    tot = 0.0
    for i in range(len(ourlist)):
        tot += ourlist[i][0]

    print("     Average Fitness: ", tot/popsize)
    print("     Best Fitness: ", ourlist[-1][0])

    for i in range(numgens):        #for loop for each generation

        x = int(0.1 * popsize)      #top 10% used as parents for each generation
        plist = ourlist[-x:]        #parent list 
        childlist = []
        for j in range(popsize - x):        #remaining 90% of the current programs are not needed so we cross 10% of the parents with each other and create 90% children 
            mom = random.choice(plist)[1]    #random mom
            dad = random.choice(plist)[1]   #random dad
            c = 0
            while dad == mom:               #we dont want the dad and mom to be the same, so we ensure they arent 
                dad = random.choice(plist)[1]
                c+=1
                if c > 20:                  #this occurs if all the 10% of the parents are the same, so we mutate them
                    dad.mutate()            #if dads are all the same, then we mutate and hope to exit the loop 
                    c = 0
                
                
            
            bastard = mom.crossover(dad)    
            mff = random.choice(range(3))   #each child has a 1 in 3 chance of being mutated

            if mff == 0:        
                for r in range(5):          #if child is chosen to be mutated, we mutate them five times 
                    bastard.mutate()
            
            
            childlist += [bastard]          #list of children programs of picobot 
        
        newPList = [plist[x][1] for x in range(len(plist))]         #removing fitness from the plist so we can add to childlist
        generations = childlist + newPList                      #full list of next generation of children and parents 

        
        LC = [(evaluateFitness(generations[e], trials, steps), generations[e]) for e in range(popsize)]
        
        ourlist = sorted(LC)        #sorting into order again 
        print("Generations: " ,i+1 )        #i + 1 as we have already computed one generation but i is in the previous generation 
        total = 0.0
        for y in range(len(ourlist)):
            total += ourlist[y][0]

        print("     Average Fitness: ", total/popsize)
        print("     Best Fitness: ", ourlist[-1][0])
        
    print("Best program is: \n")
    return ourlist[-1][1]

        




        


