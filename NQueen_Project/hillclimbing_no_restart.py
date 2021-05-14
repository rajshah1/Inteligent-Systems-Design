import random
import copy

class NQueenProblem(object):
    # This method calculates all the row conflicts for a queen placed in a particular cell.
    @classmethod
    def rowHits(self, a, n):
        hits = 0
        i = 0
        while i < n:
            j = 0
            while j < n:
                if i != j:
                    if a[i] == a[j]:
                        hits += 1
                j += 1
            i += 1
        return hits

    # This method calculates all the diagonal conflicts for a particular position of the queen
    @classmethod
    def diagonalHits(self, a, n):
        hits = 0
        d = 0
        i = 0
        while i < n:
            j = 0
            while j < n:
                if i != j:
                    d = abs(i - j)
                    if (a[i] == a[j] + d) or (a[i] == a[j] - d):
                        hits += 1
                j += 1
            i += 1
        return hits


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

    # This method returns total number of hits for a particular queen position
    @classmethod
    def totalHits(self, a, n):
        hits = 0
        hits = self.rowHits(a, n) + self.diagonalHits(a, n)
        return hits

    # This method calculates the conflicts for the current state of the board and quits whenever finds a better state.
    # 	 Note: This function is used for Hill Climbing algorithm
    @classmethod
    def optimalSol(self, a, n):
        global movesTotal
        hits = 0
        row = -1
        col = -1
        checkBetter = False
        best = []
        # Sets min variable to the hits of current board so that if finds better than this it will quit.
        mins = self.totalHits(a, n)
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
                    movesTotal +=1
                    #print('Queen Position',best)
                    # Assigning the queen to each position and then calculating the hits
                    hits = self.totalHits(best, n)
                    if mins > hits:
                        # If a better state is found, that particular column and row values are stored
                        col = i
                        row = j
                        mins = hits
                        checkBetter = True
                        break
                best[i] = m
                # Restoring the array to the current board position
                j += 1
            i += 1
        if col == -1 or row == -1:
            # If there is no better state found
            print("Stuck at Local Maxima with " ,hits ," hits. Now using Random restart...")
            return False
        a[col] = row
        return True
        # Returns true to the main function if there is any better state found

    # Below function generates a random state of the board
    @classmethod
    def randomGen(self, a, n):
        i = 0
        while( i < n):
            a[i] =random.randint(0,n-1) + 0
            i += 1
        

    # Below function verifies whether the current state of the board is the solution(I.e with zero conflicts)
    @classmethod
    def checkSol(self, a, n):
        if self.totalHits(a, n) == 0:
            return True
        return False

    # Below method finds the solution for the n-queens problem with Min-Conflicts algorithm
    @classmethod
    def minConflict(self, b, n, iterations):
        store = []
        self.fillList(store, n)
        randomCount = 0
        movesTotal = 0
        movesSolution = 0
        row = 0
        maxSteps = iterations
        # The maximum steps that can be allowed to find a solution with this algorithm
        while not self.checkSol(b, n):
            # Loops until it finds a solution, 
            randomSelection = random.randint(0,len(store)-1) + 0
            # Randomly selects a column from the available
            currentValue = b[store[randomSelection]]
            # This stores the current queue position in the randomly selected column
            randomValue = store[randomSelection]
            mins = self.hitsMinConflict(b, n, randomValue)
            # Sets the minimum variable to the current queue hits
            min_compare = mins
            while(not store):
                store.remove(randomSelection)
            i = 0
            while i < n:
                if currentValue != i:
                    b[randomValue] = i
                    col = self.hitsMinConflict(b, n, randomValue)
                    # Calculates the hits of the queen at particular position
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
                    self.randomGen(b, n)
                    self.fillList(store, n)
                    maxSteps = iterations
            else:
                # When we find the the position in the column with minimum conflicts
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
    
        print("Number of Moves in the solution set: ", movesSolution)



    # Below function returns the hits of a queen in a particular column of the board
    @classmethod
    def hitsMinConflict(self, b, n, index):
        hits = 0
        t = 0
        i = 0
        while i < n:
            if i != index:
                t = abs(index - i)
                if b[i] == b[index]:
                    hits += 1
                elif b[index] == b[i] + t or b[index] == b[i] - t:
                    hits += 1
            i += 1
        return hits

    # Below function fills the Array List with numbers 0 to n-1
    @classmethod
    def fillList(self, store, n):
        i = 0
        while i < n:
            store.append(i)
            i += 1
        return

def main():
    n = int(input("Enter the number of Queens on the board: "))
    queens = NQueenProblem()
    a = [None] * n
    queens.randomGen(a, n)
    totalRestart = 0
    movesTotal = 0
    movesSolution = 0
    
    print("How many times do you want to run the code??")
    success=0
    failure=0
    notimes = int(input("Please enter the value:"))
    while (notimes!=0):
        if queens.optimalSol(a, n):
            movesTotal += 1
            movesSolution += 1
            success+=1
            print('Solution Found')
        else:
            failure+=1
            print('No solution')
        print("Total number of moves taken: ",movesTotal)
        # Gives the total number of moves from starting point
        print("Number of moves in the solution set: ",movesSolution)
        # Gives number of steps in the solution set.
        i = 0
        print(notimes)
        notimes = notimes - 1
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
    print('Success- '+str(success))
    print('Failure- '+str(failure))
    
if __name__ == '__main__':
    main()