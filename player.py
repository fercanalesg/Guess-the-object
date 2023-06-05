import socket
import os
import sys
import time
import threading
import sqlite3

PROTOCOL = "utf-8"
SERVER = 'localhost'
PORT = 9000

DIVISION = "--------------------------------------------------------------------------------"

connection = sqlite3.connect('projectdb.db')
cursor = connection.cursor()
check = None
role = None

def cleanTerminal():                                                                        # Function to clean the terminal and have the window more clear
    os.system('cls')

def AskForGuesser(question):                                                                # Function to ask the host to type the Guesser
    while True:                                                                             # We ask the name of the guesser until it is a valid input
        guesser = input(">> ")
        if guesser.upper() in question.upper():                                             # This is to check if the typed name corresponds to an existing player
            break 
        else:
         print("Please type the name of an existing player")
    return guesser

def AskForCategory():
    while True:                                                                             # We ask the host to choose the category
        cat = input(">> ")
        try:
            if int(cat) in [1,2,3,4,5,0]:
                break
            else:
                print("Please type a valid option ")
        except ValueError:
            print("Please type a valid option ")
         
    return cat

def blinkingText(text):                                                                     # Function to display a blinking message
    while check != '':
        sys.stdout.write("\r" + text)                                                       # Writes the text in the Buffer
        sys.stdout.flush()                                                                  # Displays the text
        time.sleep(0.5)
        sys.stdout.write("\r" + " " * len(text))
        sys.stdout.flush()
        time.sleep(0.5)

def waitForENTER():                                                                         # We create a thread for the 'waiting for Enter' function to run parallel to the main thread
    global check
    blink_thread = threading.Thread(target=blinkingText, args=("Press ENTER to continue",))
    blink_thread.start()
    check = input()                                     
    blink_thread.join()                                                                     # We stop the next lines of codes until the user hits ENTER
    check = None

def previousQuestions(response):                                                            # Function to print all the previous questions and answers so that each of the player can see them               
    retrieveData = cursor.execute("SELECT * FROM gameTable")                                # We retrieve all the questions and answers that has been saved in our database
    for row in retrieveData:
        print("-"*(len(row[1])+len(row[2]))*3)
        print(f"{row[0]} | {row[1]} | {row[2]}")
        print("-"*(len(row[1])+len(row[2]))*3)

def AskForQuestion(numQ):                                                                   # Function to ask the guesser to type a question
    if numQ == possibleQuestions:                                                           # This means it is the last question, the guesser needs to type ONLY the object
        display = f"{DIVISION}\nLAST QUESTION, type the name of the object: "
    else:
        display = f"{DIVISION}\nQuestion {numQuestion}                                  "
        display += f"{possibleQuestions-numQ} questions left\nType a question: "
    return display


def AskForAnswer(numQuestion):                                                              # Function to ask the chooser to answer the question
    while True:
        answer = input(f"{DIVISION}\nAnswer {numQuestion}\nType your answer: ")
        if answer.upper() in ['Y', 'N', 'S']:                                               # The chooser should only be allowed to answer with Y, N or S, refering to -> Yes / No / Sometimes
            break 
        else:
            print("Invalid input. Please type 'Y', 'N' or 'S' ")                            # If we get an invalid input, we ask again for the answer
    
    if answer.upper() == "Y":                                       
        return "YES"
    elif answer.upper() == "N":                                                             # The chooser will answer just with a letter, but we are sending the full word to the guesser, for it to be more clear
        return "NO"
    else:
        return "SOMETIMES"


def makeMove(role, numQuestion):                                                            # Function for each of the players to do their move, answering or asking
    if role == 'G':
        client.sendall(input(AskForQuestion(numQuestion)).encode(PROTOCOL)) 
        response = client.recv(512).decode(PROTOCOL)
        cleanTerminal()
        previousQuestions(response)
        
    else:
        client.sendall(AskForAnswer(numQuestion).encode(PROTOCOL))
        response = client.recv(512).decode(PROTOCOL)
        cleanTerminal()
        print("Secret Object: " + object.upper())                                           # Only the chooser is able to see the secret object while the game is running
        previousQuestions(response)
        print(f"\n{response}")
        
    if "Game Over" in response:
        if role == 'C':
            client.sendall('OVER'.encode(PROTOCOL))
        else:
            print(response)
        return True
    return None

        
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

cleanTerminal()                                             # We clean the terminal when we run the code

name = input("Please type your name \n >> ")    
client.sendall(name.encode(PROTOCOL))                       # We send the client's name
cleanTerminal()
numberOfPlayer = int(client.recv(1024).decode(PROTOCOL))
print(f"{name}, you are player {numberOfPlayer}")
client.sendall("Ok".encode(PROTOCOL))                       # We send an approval of connection to separate two 'recv'
run = True

print(f"{client.recv(512).decode(PROTOCOL)}")               # This lines receive the introducing message
time.sleep(2)
cleanTerminal()
client.sendall("Ok".encode(PROTOCOL)) 
#################################################

while run:
    print(client.recv(512).decode(PROTOCOL))                           # Host receives the list of categories and the other player receives a waiting message
    if numberOfPlayer == 0:
        cat = AskForCategory()
        client.sendall(cat.encode(PROTOCOL))                  # The host sends the chosen category number
        GuesserQuestion = client.recv(512).decode(PROTOCOL)             # This receives the message 'Who is going to be the guesser', with the name of the two players             
        if GuesserQuestion == "Exit":                                   # If the client receives "Exit", means he/she decided to quit the game, so this is going to close the client connection and terminate the program
            print("You have quit the game")
            client.close()
            break
        print(GuesserQuestion)                                          # We print the question
        guesser = AskForGuesser(GuesserQuestion)
        client.sendall(guesser.encode(PROTOCOL))
        
    role = client.recv(512).decode(PROTOCOL)
    if role == "Exit":                                                     # The player that is not the host will receive an "Exit" message if the host quit the game
        print("The host quit the game")
        client.close()
        break                   
    cleanTerminal()
    print(role[2:])                                                         # We just want to print the message, because the first 2 indexes contain the number of possible questions and the letter of Guesser or Chooser (G or C)
    possibleQuestions = int(role[1])                                        # The index [1] is the number of possible questions, and we convert it to int
    role = role[0]                                                          # The letter of the role is the index [0] from our retrieve message
    

    if role == 'C':
        object = input(">> ")
        client.sendall(object.encode(PROTOCOL))
    else:
        print("Waiting for the CHOOSER to type the object...\n")

    ######################### THE GAME STARTS #########################
    while True:
        currentTurn = client.recv(512).decode(PROTOCOL)
        numQuestion = int(currentTurn[1])
        if currentTurn[0] == role:
            move = makeMove(role, numQuestion)
            if move:
                break
        else:
            print("Waiting for the question...\n")
            response = client.recv(512).decode(PROTOCOL)
            print(f"{response}")
            if "Game Over" in response:
                client.sendall("OVER".encode(PROTOCOL))
                break
    
    waitForENTER()
    cleanTerminal()
    client.sendall("CONTINUE".encode(PROTOCOL))





