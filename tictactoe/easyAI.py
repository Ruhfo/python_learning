import tkinter
import random

class Easy_AI():
    def __init__(self, side):
        self.side = side
        print(self.side)
    def move(self, grid):
        #Basic AI decision-making logic
        myTokens = []
        enemyTokens = []
        free = []
        for x in range(3):
            for y in range(3):
                member = grid[x][y]
                newTuple = (x,y, grid[x][y])
                if member[0].get() == self.side:
                    myTokens.append(newTuple)
                elif member[0].get() == " ":
                    free.append(newTuple)
                else:
                    enemyTokens.append(newTuple)

        #Can we win with this move?
        print("free:", len(free), "enemy:", len(enemyTokens), "own:", len(myTokens))
        solution = self.winning_move(grid, myTokens, free)
        if solution[0] == True:
            return solution[1]
        solution = self.winning_move(grid, enemyTokens, free)
        if solution[0] == True:
            return solution[1]
        #Can enemy win with his next move

        cell = random.choice(free) 
        return cell[2]
    def winning_move(self, grid, tokens, free):
        #Checking if it is possible to win with one move
        for i in range(len(tokens)):
            token = tokens.pop()
            for other in tokens:
                if other[0] == token[0]: #Checking winning chance for rows
                    for i in [0,1,2]:
                        if i not in (other[1], token[1]):
                            y = i
                    x = token[0]
                    if (x, y, grid[x][y]) in free:
                        print("solution row")
                        return (True, grid[x][y])
                if other[1] == token[1]: #Checking winning chance for collumns
                    for i in [0,1,2]: 
                        if i not in (other[0], token[0]):
                            x = i
                    y = token[1]
                    if (x, y, grid[x][y]) in free:
                        print("solution collumn")
                        return (True, grid[x][y])

                if abs(other[0]-token[0]) == abs(other[1]-token[1]): #checking winning chance diagonaly
                    for i in [0,1,2]:
                        if i not in (other[0], token[0]):
                            x = i
                        if i not in (other[1], token[1]):
                            y = i
                    if (x, y, grid[x][y]) in free:
                        print("Solution diagonal")
                        return(True, grid[x][y])
        print("Flipping false")
        return (False, "" )
