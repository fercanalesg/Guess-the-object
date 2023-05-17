import time

class Game:
    def __init__(self,):
        self.currentGuesser = ''
        self.currentChooser = ''
        self.secretObject = ''

        self.currentCategory = None

        self.ready = True
        

        self.allowedAnswers = ["YES", "NO", "SOMETIMES"]

        self.categories = ["Tools and equipement", "Sports", "House Objects", "Animals", "Clothing and accesories"]
        self.possibleQuestions = {1:3, 2:8 ,3:7 , 4:6, 5:6}

        self.cont = False
        self.startGame = False


    def introducingMessage(self, p, names):
        if p == 0:
            while len(names) == 1:
                pass
            return f"You are playing with {names[1]}"
        else:
            while len(names) == 1:
                pass
            return f"You are playing with {names[0]}\n"
        
    def choosingCategoryMessage(self,p):
        start = time.perf_counter()
        if p == 0:
            message = "Choose the category please:\n"
            for i, cat in enumerate(self.categories):
                message += f"{i+1} {cat} ({self.possibleQuestions[i+1]} questions)\n"
            print(f"p = 0 --- {time.perf_counter() - start}")
        else:
            self.ready = False
            print(f"p = 1 --- {time.perf_counter() - start}")
            message = "The host is preparing the game..."
        return message
    
    def choosingRolesMessage(self, names):
        return f"Who is going to be the Guesser,  {names[0]} or {names[1]}?"

    def chooseCategory(self, p):
        pass

    def setRolesAndCategory(self, names, category, guesser):
        self.currentCategory = category
        self.currentGuesser = guesser
        self.currentChooser = names[0] if self.currentGuesser == names[1] else names[1]
        print(f"GUESSER: {self.currentGuesser}")
        print(f"CHOOSER: {self.currentChooser}")

    def checkWinner(self):
        return False
    
    def choosingObjectMessage(self, names, player):
        if names[player] == self.currentChooser:
            message = f"CYou are the CHOOSER, the category is '{self.categories[self.currentCategory-1]}'\nPlease choose the secret object according to the category\n"
        else:
            message = f"GYou are the GUESSER, the category is '{self.categories[self.currentCategory-1]}',\nYou will have {self.possibleQuestions[self.currentCategory]} questions to guess the object\n"
        return message

    def setObject(self, object):
        self.secretObject = object

