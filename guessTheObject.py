import time
import os

class Game:
    def __init__(self,):
        self.currentGuesser = ''
        self.currentChooser = ''
        self.secretObject = ''

        self.winner = None
        self.currentCategory = None

        self.question = None
        self.answer = None

        self.ready = True
        
        self.categories = ["Tools and equipement", "Sports", "House Objects", "Animals", "Clothing and accesories"]
        self.possibleQuestions = {1:3, 2:8 ,3:7 , 4:6, 5:6}

        self.cont = False
        self.startGame = False


    def introducingMessage(self, p, names):
        if p == 0:
            while len(names) == 1:                                  # We wont send the introducing message until both players are connected
                pass
            return f"You are playing with {names[1]}"
        else:
            while len(names) == 1:
                pass
            return f"You are playing with {names[0]}\n"
        
    def choosingCategoryMessage(self,p):
        if p == 0:
            message = "Choose the category please:\n"
            for i, cat in enumerate(self.categories):                                       # This is to make a list of the possible categories, each with their possible questions
                message += f"{i+1} {cat} ({self.possibleQuestions[i+1]} questions)\n"
        else:
            self.ready = False
            message = "The host is preparing the game..."                                   # If the player is not the host, he/she will receive a waiting message
        return message
    
    def choosingRolesMessage(self, names):
        return f"Who is going to be the Guesser,  {names[0]} or {names[1]}?"                 # We send the question for the host, for him/her to choose the guesser


    def setRolesAndCategory(self, names, category, guesser):                                 # Function to set roles and category, already chosen by the host
        self.currentCategory = category
        self.currentGuesser = guesser
        self.currentChooser = names[0] if self.currentGuesser == names[1] else names[1]
        print(f"GUESSER: {self.currentGuesser}")                                            # We print the roles in the server terminal
        print(f"CHOOSER: {self.currentChooser}")

    def checkWinner(self):
        return False
    
    def choosingObjectMessage(self, names, player):                                            # Function to send the corresponding message to each of the players, according to the chosen roles
        if names[player] == self.currentChooser:
            message = f"C{self.possibleQuestions[self.currentCategory]}You are the CHOOSER, the category is '{self.categories[self.currentCategory-1]}'\nPlease choose the secret object according to the category\n"    # Index 0 is the role, and index 1 is the possible number of questions
        else:
            message = f"G{self.possibleQuestions[self.currentCategory]}You are the GUESSER, the category is '{self.categories[self.currentCategory-1]}',\nYou will have {self.possibleQuestions[self.currentCategory]} questions to guess the object\n"
        return message

    def setObject(self, object):                                                                # Function to set the secret object, chosen by the chooser
        self.secretObject = object

    def resetGame(self):                                                                        # Function to reset the whole game, to start a new one
        os.system('cls')
        self.currentGuesser = ''
        self.currentChooser = ''
        self.secretObject = ''

        self.currentCategory = None
        self.cont = False
        self.startGame = False
