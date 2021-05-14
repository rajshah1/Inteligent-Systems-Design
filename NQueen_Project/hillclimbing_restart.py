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

    # This method returns total number of hits for a particular queen position
    @classmethod
    def totalHits(self, a, n):
        hits = 0
        hits = self.rowHits(a, n) + self.diagonalHits(a, n)
        return hits

    # This method calculates the conflicts for the current state of the board and quits whenever finds a better state.
    @classmethod
    def optimalSol(self, a, n):
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
            print("Stuck at Local Maxima with " ,hits ,"hits. now using random restart...")
            return False
        a[col] = row
        return True

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

def main():

    totalRestart = 0
    movesTotal = 0
    movesSolution = 0


        # Randomly generate the board

        # The below code will be executed if the user chooses he options 1 or 3(n-queen with Hill Climbing method)
    n = int(input("Enter the number of Queens on the board: "))

    a = [None] * n
    queens = NQueenProblem()
    queens.randomGen(a, n)

    while not queens.checkSol(a, n):
                # Executes until a solution is found
        if queens.optimalSol(a, n):
                    # If a better state for a board is found
            movesTotal += 1
            movesSolution += 1
            continue
        else:
                    # If a better state is not found
            movesSolution = 0
            queens.randomGen(a, n)
                    # Board is generated Randomly
            totalRestart += 1
    print("Total number of Restarts: ",totalRestart)
    print("Total number of moves taken: ",movesTotal-1)
    # Gives the total number of moves from starting point
    print("Number of moves in the solution set: ",movesSolution)
    # Gives number of steps in the solution set.
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
        print("Average steps",movesTotal)
    else:
        print("Average steps",movesTotal/totalRestart)

if __name__ == '__main__':
    main()