import random
import time
import copy

class NQueenProblem(object):
    # This method calculates all the row conflicts for a queen placed in a particular cell.
    @classmethod
    def rowCollisions(self, a, n):
        collisions = 0
        i = 0
        while i < n:
            j = 0
            while j < n:
                if i != j:
                    if a[i] == a[j]:
                        collisions += 1
                j += 1
            i += 1
        return collisions


    # This method calculates all the diagonal conflicts for a particular position of the queen
    @classmethod
    def diagonalCollisions(self, a, n):
        collisions = 0
        d = 0
        i = 0
        while i < n:
            j = 0
            while j < n:
                if i != j:
                    d = abs(i - j)
                    if (a[i] == a[j] + d) or (a[i] == a[j] - d):
                        collisions += 1
                j += 1
            i += 1
        return collisions

    # This method returns total number of collisions for a particular queen position
    @classmethod
    def totalCollisions(self, a, n):
        collisions = 0
        collisions = self.rowCollisions(a, n) + self.diagonalCollisions(a, n)
        return collisions

    # This method calculates the conflicts for the current state of the board and quits whenever finds a better state.
    # 	 Note: This function is used for Hill Climbing algorithm
    @classmethod
    def bestSolution(self, a, n):
 #       min = int()
        collisions = 0
        row = -1
        col = -1
  #      m = int()
        checkBetter = False
        best = []
        # Sets min variable to the collisions of current board so that if finds better than this it will quit.
        mins = self.totalCollisions(a, n)
        best = copy.deepcopy(a)
        # Create a duplicate array for handling different operations
        i = 0
        while i < n:
            # This iteration is for each column
            if checkBetter:
                # If it finds and better state than the current, it will quit
                break
            m = best[i]
            j = 0
            while j < n:
                # This iteration is for each row in the selected column
                if j != m:
                    # This condition ensures that, current queen position is not taken into consideration.
                    best[i] = j
                
                    #self.printBoard(best,n)
                    #print('HI',best)
                    # Assigning the queen to each position and then calculating the collisions
                    collisions = self.totalCollisions(best, n)
                    if mins > collisions:
                        # If a better state is found, that particular column and row values are stored
                        col = i
                        row = j
                        mins = collisions
                        checkBetter = True
                        break
                best[i] = m
                # Restoring the array to the current board position
                j += 1

            i += 1
        if col == -1 or row == -1:
            # If there is no better state found
            print("Reached Local Maxima with " ,collisions ," Regenerating randomly")
            return False
        a[col] = row
        return True
        # Returns true to the main function if there is any better state found

    @classmethod
    def printBoard(self,best,n):
        i = 0
        while i < n:
            j = 0
            while j < n:
                if j == best[i]:
                    print(" Q ", end="")
                else:
                    print(" - ", end="")
                j += 1
            print()
            i += 1
    
    
    
    # Below function generates a random state of the board
    @classmethod
    def randomGenerate(self, a, n):
        # gen = Random()
        # i = 0
        # while i < n:
        #     a[i] = gen.get(n) + 0
        #     i += 1

        i = 0
        while( i < n):
            a[i] =random.randint(0,n-1) + 0
            i += 1
        

    # Below function verifies whether the current state of the board is the solution(I.e with zero conflicts)
    @classmethod
    def isSolution(self, a, n):
        if self.totalCollisions(a, n) == 0:
            return True
        return False

    # Below method finds the solution for the n-queens problem with Min-Conflicts algorithm
    @classmethod
    def minConflict(self, b, n, iterations):
        # This array list is for storing the columns from which a random column will be selected
   #     store = ArrayList()
        store = []
        self.fillList(store, n)

        randomCount = 0
        movesTotal = 0
        movesSolution = 0
        row = 0
        maxSteps = iterations
        # The maximum steps that can be allowed to find a solution with this algorithm
        while not self.isSolution(b, n):
            # Loops until it finds a solution, 
            randomSelection = random.randint(0,len(store)-1) + 0
            # Randomly selects a column from the available
            currentValue = b[store[randomSelection]]
            # This stores the current queue position in the randomly selected column
            randomValue = store[randomSelection]
            mins = self.collisionsMinConflict(b, n, randomValue)
            # Sets the minimum variable to the current queue collisions
            min_compare = mins
    #        print("len store: ",len(store)-1,"randomSelection: ",randomSelection," currentValue: ",currentValue," randomValue: ",randomValue," mins: ",mins," min_compare: ",min_compare)
            while(not store):
                store.remove(randomSelection)
            i = 0
            while i < n:
                if currentValue != i:
                    b[randomValue] = i
                    col = self.collisionsMinConflict(b, n, randomValue)
                    # Calculates the collisions of the queen at particular position
                    if col < mins:
                        mins = col
                        row = i
                i += 1
            if min_compare == mins:
                # When there is no queen with minimum conflicts than the current position
                if maxSteps != 0:
                    # Checks if the maximum steps is reached
                    if len(store) >= 0:
                        # checks whether there are columns available in the Array List
                        b[randomValue] = currentValue
                        # restores the queen back to the previous position
                        maxSteps -= 1
                    else:
                        self.fillList(store, n)
                else:
                    # If the max steps is reached then, the board is regenerated and initiated the max steps variable
                    randomCount += 1
                    movesSolution = 0
                    self.randomGenerate(b, n)
                    self.fillList(store, n)
                    maxSteps = iterations
            else:
                # When we find the the position in the column with minimum conflicts
                movesTotal += 1
                movesSolution += 1
                b[randomValue] = row
                min_compare = mins
                store.clear()
                maxSteps -= 1
                self.fillList(store, n)
        print()
        i = 0
        count = 0
        while i < n:
            j = 0
            while j < n:
                if j == b[i]:
                    print(" Q ", end="")
                else:
                    print(" - ", end="")
                j += 1
                
            print()
            i += 1
        print("Total number of Random Restarts: ",randomCount)
        print("Total number of Moves: ", movesTotal)
        print("Number of Moves in the solution set: ", movesSolution)

    # Below function returns the collisions of a queen in a particular column of the board
    @classmethod
    def collisionsMinConflict(self, b, n, index):
        collisions = 0
        t = 0
        i = 0
        while i < n:
            if i != index:
                t = abs(index - i)
                if b[i] == b[index]:
                    collisions += 1
                elif b[index] == b[i] + t or b[index] == b[i] - t:
                    collisions += 1
            i += 1
        return collisions

    # Below function fills the Array List with numbers 0 to n-1
    @classmethod
    def fillList(self, store, n):
        i = 0
        while i < n:
            store.append(i)
            i += 1
        return



totalRestart = 0
movesTotal = 0
movesSolution = 0

print("Please select one from the below options:")
print("1. Min Conflict method with random restart")
print("2.exit")
choice = int(input("Please enter the choice:"))


        # Randomly generate the board

        # The below code will be executed if the user chooses he options 1 or 3(n-queen with Hill Climbing method)
if choice == 1:
    n = int(input("Please enter the value of n:"))
    if (n > 1 and n < 4) or n <= 1:
        print("*Please choose n value either greater than 3 or equals to 1 - Program Terminated")
        exit()    
    if choice < 1 or choice > 7:
        print("*Program terminated - Wrong option selected")
        exit()
    a = [None] * n
    b = [None] * n
    queens = NQueenProblem()
    queens.randomGenerate(a, n)
    b = copy.deepcopy(a)
    print("**********Sideways with Random Restart*********")
    startTime = time.time()
    while not queens.isSolution(a, n):
                # Executes until a solution is found
        if queens.bestSolution(a, n):
                    # If a better state for a board is found
            movesTotal += 1
            movesSolution += 1
            continue 
        else:
                    # If a better state is not found
            movesSolution = 0
            queens.randomGenerate(a, n)
                    # Board is generated Randomly
            totalRestart += 1
    endTime = time.time()
    print("Number of Restarts: ",totalRestart)
    print("Total number of moves taken: ",movesTotal)
    # Gives the total number of moves from starting point
    print("Number of moves in the solution set: ",movesSolution)
    # Gives number of steps in the solution set.
    print("Time Taken in milli seconds: ",(endTime - startTime))
    i = 0
    while i < n:
        j = 0
        while j < n:
            if j == a[i]:
                print(" Q ", end="")
            else:
                print(" - ", end="")
            j += 1
        print()
        i += 1

    if(totalRestart == 0):
         print(" average steps",movesTotal)
    else:
         print("Average restarts:",(movesTotal)/totalRestart)
        # If the Min-Conflict algorithm is selected
if choice == 2:
    exit()

