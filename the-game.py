#!/usr/bin/env python3

#######################################
# Autor: Andres Jõgi                  #
# Programm: Lihtne trips-traps-trull  #
# kirjutatud: 2015                    #
# Täiendused: 2017                    #
#######################################


#Kasutame tkinter (kasutajaliidese jaoks) 
#random ja
#basic_AI(ise kirjutatud) ehk arvuti poolt kontrollitud vastase lisamooduleid

import tkinter as tk
import tkinter.messagebox
import random
from basicAI import Basic_AI

class Game():
    """Kogu rakenduse põhi klass, loob tkinter akna ja mänguvälja sinna sisse """
    def __init__(self):
        #Tekitame akna mänguväljaga ja initseerime mängu jaoks vajalikud muutujad

        self.window= tk.Tk()
        self.window.wm_title("Tic-tac-toe")
        
        self.gameFrame = tk.Frame(self.window) #Frame containing 3x3 array of cell buttons
        self.gameFrame.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True)

        #Tekitame mänguvälja 3x3 maatriksi 
        self.grid = [[[tk.StringVar(), tk.Button()] for i in range(3)] for i in range(3)]
        self.currentPlayer = " " #Muutuja mängija sümboliga

        #self.botEnabled = True #Kas mängu mängivad kaks mängijat või käib mäng arvuti vastu, (hetkel kasutu)
        
        self.init_game()
        self.window.mainloop()
    def init_game(self):
        #Joonistame mänguruudustiku aknasse ja alustame mängu ennast
        for x in range(3):
            for y in range(3):
                
                #joonistame aknasse nupud 3x3 maatriksisse
                self.grid[x][y][0].set(" ") #Kõik mänguväljad on esialgu vabad, ehk nendele pole kirjutatud ei X ega Y
                
                #konfigureerime tkinteri Frame sedasi, et elemendid paigutuvad sinna sisse ruudustiku järgi
                self.gameFrame.columnconfigure(y, weight=1)
                self.gameFrame.rowconfigure(x, weight=1)
                
                #Lisame ruudustikku nupu
                #parameetri command väärtuseks omistame lambdafunktsiooni, mida tahame nupu vajutuse peale välja kotsuda
                self.grid[x][y][1]=tk.Button(self.gameFrame, textvariable=self.grid[x][y][0], font=('Sans-serif', 24, "bold"),  command= lambda cell = self.grid[x][y]: self.move(cell), bg = "#002b36", fg= "RED")

                self.grid[x][y][1].grid(row=y, column=x, sticky=tk.N+tk.S+tk.W+tk.E)
        
        #Defineerime mängijate sümbolid
        self.players = ("X", "O") 
        self.currentPlayer = random.choice(self.players)

        #Muutuja, mis näitab, kas on arvuti kord või mitte
        self.bot = False 

        #Vastavalt Mängija saadud sümbolile tekitame vastase objekti ja anname talle tema sümboli
        if self.currentPlayer == "X":
            self.aiPlayer = Basic_AI("O")
        else:
            self.aiPlayer = Basic_AI("X")

    def move(self, cell):
        #Salvestame mängija käibud listi

        cell[0].set(self.currentPlayer) #Muudame nupu teksti mängija sümboliks
        cell[1].configure(state=tk.DISABLED) #Ei luba juba hõivatud mänguvälja üle kirjutada
        
        #Teise mängija kord
        if self.bot == True:
            self.bot = False
        else:
            self.bot = True

        #Kontrollime, kas mäng on võidetud
        self.game_checker()

    def ai_move(self):
        #Laseme arvutil teha käigu
        cell = self.aiPlayer.move(self.grid) 
        #Lõpetame käigu
        self.move(cell)

    def game_checker(self):
        #Kontrollfunktsioon, võitja või viigi tuvastamiseks
        grid = self.grid 
        
        #check rows and collumns if someone has won
        for i in range(3):
            if grid[i][0][0].get() == grid[i][1][0].get() == grid[i][2][0].get() != " ":
                #veerg on täis
                self.victory(True)
                return 
            if grid[0][i][0].get() == grid[1][i][0].get() == grid[2][i][0].get() != " ":
                #rida on täis
                self.victory(True)
                return 
        #Checking diagonals
        if grid[0][0][0].get() == grid[1][1][0].get() == grid[2][2][0].get() != " ":
            #diagonaali kaudu on võit
            self.victory(True)
            return 
        if grid[2][0][0].get() == grid[1][1][0].get() == grid[0][2][0].get() != " ":
            #diagonaali kaudu on võit
            self.victory(True)
            return 

        #Kontrollime kas mänguväljal on veel vabasi ruute
        free = []
        for row in grid:
            for cell in row:
                if cell[0].get() is " ":
                    free.append(cell[0].get())
        if " " not in free:
            self.victory(False) #Viik
            return

        #Teise mängija kord
        if self.currentPlayer == self.players[0]:
            self.currentPlayer = self.players[1]
        else:
            self.currentPlayer = self.players[0]

        #Kui eelmise mängu tegi mängija on vastase kord
        if self.bot == True:
            self.ai_move()
    def victory(self, status):
        #Kuvame mängu lõpptulemuse
        if status is True:
            tkinter.messagebox.showinfo("Game over", "Player {:s} has won".format(self.currentPlayer)) 
        else:
            tkinter.messagebox.showinfo("Game over", "It's a draw") 

        if tkinter.messagebox.askquestion(title="question", message="Do you want to start a new game?") == "yes":
            self.init_game() #Küsime kas mängija tahab uuesti alustada
        else:
            self.window.destroy() #Sulgeme akna
if __name__ == "__main__":
    #Antud valikulause käivitub ainult siis kui fail käivitatakse põhiprogrammina
    #Ehk siis saame klassi Game importida ka mõnda teise rakendusse ja seda seal kasutada
    game = Game()
