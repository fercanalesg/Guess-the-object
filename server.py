import socket
import threading
import time
import os
import sys
import sqlite3

from guessTheObject import Game

PROTOCOL = 'utf-8'

server = 'localhost'
port = 9000
os.system('cls')

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((server, port))
s.listen()

mainConnection = sqlite3.connect('projectdb.db')
mainCursor = mainConnection.cursor()

print("Waiting for a connection, Server Started")
names = []
players = []
Chooser = 'C'
Guesser = 'G'
counter = 1

def sendToOtherPlayer(conn, message):                                                  # Function to send the move to the other player
    for player in players:
        if player != conn:
            try:
                player.sendall(message.encode(PROTOCOL))
            except:
                pass

def sendTurn(conn, p):                                                                 # Function to send each of the players the current turn and also the number of question/answer for them to be aware
    for player in players:
        if player != conn:
            if names[p] == game.currentGuesser:                                        # If the current player is the guesser, we are going to send a 'C' to the Chooser to notify it is his/her turn
                nextTurn = Chooser
            else:
                nextTurn = Guesser
            player.sendall((nextTurn+str(counter)).encode(PROTOCOL))

def checkWinner(number, response):                                                     # Function that checks if there is a winner
    if game.secretObject.upper() == response.upper():                                  # If the question from the guesser is equal to the secret object, then he/she guessed
        return game.currentGuesser
    elif number == game.possibleQuestions[game.currentCategory]:                       # If the guesser ran out of possible questions, the chooser wins
        return game.currentChooser
    else:
        return None
    

def cleanTable():
    temporalConnection = sqlite3.connect('projectdb.db')
    temporalCursor = temporalConnection.cursor()   
    temporalCursor.execute("DELETE FROM gameTable")

    temporalConnection.commit()
    temporalCursor.close()
    temporalConnection.close()

def handle_client(conn, p): 
    
    ######################### INTRODUCTION MESSAGES ######################
    global counter

    name = conn.recv(512).decode(PROTOCOL)                                              # We recover the clients name
    names.insert(p, name)                                                               # We insert the name of the player in the corresponding index
    print(f"{name} is player {p}")
    conn.sendall(str(p).encode(PROTOCOL))                                               # We send the number of player
    conn.recv(512).decode(PROTOCOL)                                                     # We just receive the approval of connection
    conn.sendall(game.introducingMessage(p, names).encode(PROTOCOL))                    # We send the introducing message
    conn.recv(512).decode(PROTOCOL)
    if p == 0:
        connection1= sqlite3.connect('projectdb.db')                                      # We create two connections and cursors, to be able to execute sqlite commands in both threads
        cursor1= connection1.cursor()
    else:
        connection2= sqlite3.connect('projectdb.db')
        cursor2= connection2.cursor()

    while True:
        ######################## PREPARING THE GAME ##########################
        cleanTable()                                                                    # We clean the table everytime a new game starts
        counter = 1                                                                     # counter of questions
        conn.sendall(game.choosingCategoryMessage(p).encode(PROTOCOL))                  # We send the corresponding message to each of the players, the host and the other
        time.sleep(2) 
        if p == 0:
            category = int(conn.recv(512).decode(PROTOCOL))
            if category == 0:                                                           # If category is 0, means the host decided to quit the game   
                print(f"Players have left the game...")
                sendToOtherPlayer(conn, "Exit")
                conn.sendall("Exit".encode(PROTOCOL))
                playerConnection.close()
                game.cont = True
                break
            conn.sendall(game.choosingRolesMessage(names).encode(PROTOCOL))
            guesser = conn.recv(512).decode(PROTOCOL)                                   # This receives the chosen player to be the guesser
            game.setRolesAndCategory(names,category, guesser)                     
            game.cont = True                                                            # This variable will be set to True once the host has chosen category and roles
        else:
            while not game.cont:                                                        # The second client must wait until the host prepares the game Category and chooses the Guesser
                pass
        
        if not game.currentCategory:
            playerConnection.close()
            break
        conn.sendall(game.choosingObjectMessage(names, p).encode(PROTOCOL))
        time.sleep(2)
        if name == game.currentChooser:
            object = conn.recv(512).decode(PROTOCOL)                                    # This receives the chosen object by the Chooser
            game.setObject(object)
            game.startGame = True
        else:
            while not game.startGame:                                                   # The Guesser needs to wait until the Chooser chooses the object
                pass

        time.sleep(1)

        ############################## THE GAME STARTS ###################################
        
        conn.sendall((Guesser+str(counter)).encode(PROTOCOL))                           # We send the Guesser letter cause we always start the game with a question
        
        while True:
            
            response = conn.recv(512).decode(PROTOCOL)                                  # This line is going to receive the Questions/Answers from the players
            
            if name == game.currentGuesser:                                             # Everytime the Guesser makes a question, we check if he/she guessed the object
                game.winner = checkWinner(counter, response)                            # Function that checks if there is a winner everytime it receives a response from the GUESSER
                if not game.winner:                                                     # If there is no winner, the game continues
                    game.question = response
                    print(f"{counter} {name}: {response}")
                    sendToOtherPlayer(conn, response)                                   # We forward the Question/Answer to the other player
                    time.sleep(1)
                    sendTurn(conn,p)                                                    # We send the turn 'G' or 'C'
                elif game.winner == name:                                           
                    winnerMessage = f"Game Over, you guessed the object! ----> '{game.secretObject}'"
                    nonWinnerMessage = f"Game Over, {name} guessed the object :("
                    conn.sendall(winnerMessage.encode(PROTOCOL))                        # If the Guesser won, we send him/her the winner Message
                    sendToOtherPlayer(conn, nonWinnerMessage)                           # If the Guesser won, we send the other player the nonWinner message
                    break
                else:
                    winnerMessage = f"Game Over, {game.currentGuesser} didn't guessed the object, you won! "
                    nonWinnerMessage = f"Game Over, you didn't guessed the object -----> {game.secretObject}"
                    conn.sendall(nonWinnerMessage.encode(PROTOCOL))
                    sendToOtherPlayer(conn, winnerMessage)
                    break    
            else:
                if response != "OVER":                                              
                    game.answer = response
                    if p == 0:
                        cursor1.execute("INSERT INTO gameTable VALUES(?,?,?)", (counter, game.question, game.answer))           # We use the corresponding cursor depending on the player to insert the data into the table
                        connection1.commit()
                    else:
                        cursor2.execute("INSERT INTO gameTable VALUES(?,?,?)", (counter, game.question, game.answer))
                        connection2.commit()
                    counter +=1
                    sendToOtherPlayer(conn, response)                       # We forward the Question/Answer to the other player
                    time.sleep(1)
                    sendTurn(conn,p)                                        # We send the turn to the client, we send a 'G' or 'C'
                else:
                    break
        
        game.resetGame()
        Enter = conn.recv(512).decode(PROTOCOL)
        

##################### CLIENTS CONNECTIONS #####################
p = 0
while p < 2:                                                                            # We only allow 2 connections to our server
    playerConnection, addr = s.accept()
    print(f"Connection {p}, Connected to: {addr}")
    players.append(playerConnection)                                                    # We append each connection to our list of players
    if p == 0:                                                                          # If it is the first client, we create a new game
        game = Game()
        mainCursor.execute('''CREATE TABLE IF NOT EXISTS gameTable                      
                        (number integer, question text, answer text)''')                # We create a table in case it does not exist already
    t1 = threading.Thread(target=handle_client, args=(playerConnection, p))
    t1.start ()
    p+=1

s.close()

###############################################################




