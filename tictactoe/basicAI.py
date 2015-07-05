import tkinter
import random

class Basic_AI():
    def __init__(self, side):
        self.side = side

        #Define sequence checking lambdas
        self.straight = lambda x1, x2: x1 == x2 
        self.diagonal = lambda pos1, pos2: abs(pos1[0]-pos2[0]) == abs(pos1[1]-pos2[1]) 
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
        solution = self.winning_move(grid, myTokens, free)
        if solution[0] == True:
            return solution[1]
        #Can enemy win next move
        solution = self.winning_move(grid, enemyTokens, free)
        if solution[0] == True:
            return solution[1]
        #Check for traping possibilities
        solution = self.traping_move(grid, myTokens, free)
        if solution[0] == True:
            return solution[1]
        solution = self.traping_move(grid, enemyTokens, free)
        if solution[0] == True:
            return solution[1]
        #Reasonable beginning moves
        solution = self.defaults(grid)
        if solution[0] == True:
            return solution[1]

        cell = random.choice(free) 
        return cell[2]
    def winning_move(self, grid, tokens, free):
        #Checking if it is possible to win with one move
        for i in range(len(tokens)):
            token = tokens.pop()
            for other in tokens:
                if self.straight(token[0], other[0]): #Checking winning chance for rows
                    for i in [0,1,2]:
                        if i not in (other[1], token[1]):
                            y = i
                    x = token[0]
                    if (x, y, grid[x][y]) in free:
                        return (True, grid[x][y])
                if self.straight(token[1], other[1]): #Checking winning chance for collumns
                    for i in [0,1,2]: 
                        if i not in (other[0], token[0]):
                            x = i
                    y = token[1]
                    if (x, y, grid[x][y]) in free:
                        return (True, grid[x][y])

                if self.diagonal((token[0], token[1]), (other[0], other[1])): #diagonal check
                    for i in [0,1,2]:
                        if i not in (other[0], token[0]):
                            x = i
                        if i not in (other[1], token[1]):
                            y = i
                    if (x, y, grid[x][y]) in free:
                        return(True, grid[x][y])
        return (False, "" )
    def traping_move(self, grid, tokens, free):
        for place in free:
            suitables = [] #Suitable tokens for current free cell
            for token in tokens:
                if place[0] == token[0] or place[1] == token[1] or self.diagonal((place[0], place[1]), (token[0], token[1])):
                    suitables.append(token)
            if len(suitables) >= 2:
                print("It's a trap")
                return (True, place[2])
        return(False, "")

    def defaults(self, grid):
        if  grid[1][1][0].get() is  " ":
                return (True, grid[1][1])
        for cell in (grid[0][0], grid[2][2], grid[2][0], grid[0][2]):
            if cell[0].get() is " ":
                return(True, cell)
        return(False, "")

