#!/usr/bin/env python3

#####################################
# Author: Andres Jõgi               #
# Program: simple tic-tac-toe game  #
# 2015                              #
#                                   #
#####################################
import tkinter as tk
import tkinter.messagebox
import random
from basicAI import Basic_AI

class Game():
    def __init__(self):
        self.window= tk.Tk()
        self.window.wm_title("Tic-tac-toe")
        
        self.gameFrame = tk.Frame(self.window) #Frame containing 3x3 array of cell buttons
        self.gameFrame.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True)

        #self.infoFrame = tk.Frame(self.window) #Frame containing information about the game
        #self.infoFrame.pack(side = tk.TOP, fill = tk.X, expand = False) #TODO: display some information to players

        #Creating grid for game
        self.grid = [[[tk.StringVar(), tk.Button()] for i in range(3)] for i in range(3)]
        self.currentPlayer = " " #Current player's symbol


        self.botEnabled = True
        
        self.init_game()
        self.window.mainloop()
    def init_game(self):
        #Init game
        for x in range(3):
            for y in range(3):
                #Adding actual buttons to the grid
                self.grid[x][y][0].set(" ")
                self.gameFrame.columnconfigure(y, weight=1)
                self.gameFrame.rowconfigure(x, weight=1)

                self.grid[x][y][1]=tk.Button(self.gameFrame, textvariable=self.grid[x][y][0], font=('Terminus', 24, "bold"),  command= lambda cell = self.grid[x][y]: self.move(cell), bg = "#002b36", fg= "RED")
                self.grid[x][y][1].grid(row=y, column=x, sticky=tk.N+tk.S+tk.W+tk.E)
        
        #Initialize game
        self.players = ("X", "O") 
        self.currentPlayer = random.choice(self.players)

        self.bot = False 

        if self.currentPlayer == "X":
            self.aiPlayer = Basic_AI("O")
        else:
            self.aiPlayer = Basic_AI("X")

    def move(self, cell):
        #Saving player moves to the array
        cell[0].set(self.currentPlayer)
        cell[1].configure(state=tk.DISABLED)

        if self.bot == True:
            self.bot = False
        else:
            self.bot = True

        self.game_checker()

    def ai_move(self):
        #Call ai's move function
        cell = self.aiPlayer.move(self.grid) 
        #Ending turn
        self.move(cell)

    def game_checker(self):
        #Control function for game itself
        grid = self.grid 
        
        #check rows and collumns if someone has won
        for i in range(3):
            if grid[i][0][0].get() == grid[i][1][0].get() == grid[i][2][0].get() != " ":
                #print("Yay! collumn")
                self.victory(True)
                return 
            if grid[0][i][0].get() == grid[1][i][0].get() == grid[2][i][0].get() != " ":
                #print("Yay!  row")
                self.victory(True)
                return 
        #Checking diagonals
        if grid[0][0][0].get() == grid[1][1][0].get() == grid[2][2][0].get() != " ":
            #print("Diagon alley")
            self.victory(True)
            return 
        if grid[2][0][0].get() == grid[1][1][0].get() == grid[0][2][0].get() != " ":
            #print("Diagon alley")
            self.victory(True)
            return 
        free = []
        for row in grid:
            for cell in row:
                if cell[0].get() is " ":
                    free.append(cell[0].get())
        if " " not in free:
            self.victory(False)
            return

        #Other player's turn
        if self.currentPlayer == self.players[0]:
            self.currentPlayer = self.players[1]
        else:
            self.currentPlayer = self.players[0]
        if self.bot == True:
            self.ai_move()
    def victory(self, status):
        if status is True:
            tkinter.messagebox.showinfo("Game over", "Player {:s} has won".format(self.currentPlayer)) 
        else:
            tkinter.messagebox.showinfo("Game over", "It's a draw") 

        if tkinter.messagebox.askquestion(title="question", message="Do you want to start a new game?") == "yes":
            self.init_game() #New game or what?
        else:
            self.window.destroy() #quit game
if __name__ == "__main__":
    game = Game()
