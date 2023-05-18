import socket
import threading
import pickle
import ast
import time
import os

from guessTheObject import Game

PROTOCOL = 'utf-8'

server = 'localhost'
port = 9000
os.system('cls')

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((server, port))
s.listen()

lock = threading.Lock()

print("Waiting for a connection, Server Started")
names = []
players = []
Chooser = 'C'
Guesser = 'G'
counter = 1

def sendToOtherPlayer(conn, message):
    for player in players:
        if player != conn:
            player.sendall(message.encode(PROTOCOL))

def sendTurn(conn, p):
    for player in players:
        if player != conn:
            if names[p] == game.currentGuesser:
                nextTurn = Chooser
            else:
                nextTurn = Guesser
            player.sendall((nextTurn+str(counter)).encode(PROTOCOL))

def handle_client(conn, p): 
    
    ######################### INTRODUCTION MESSAGES ######################
    global counter
    name = conn.recv(512).decode(PROTOCOL)                                   # We recover the clients name
    names.insert(p, name)
    print(f"{name} is player {p}")
    conn.sendall(str(p).encode(PROTOCOL))                                     # We send the number of player
    conn.recv(512).decode(PROTOCOL)                                           # We just receive the approval of connection
    conn.sendall(game.introducingMessage(p, names).encode(PROTOCOL))          # We send the introducing message
    conn.recv(512).decode(PROTOCOL)

    ######################## PREPARING THE GAME ##########################
    
    conn.sendall(game.choosingCategoryMessage(p).encode(PROTOCOL))
    time.sleep(2) 
    if p == 0:
        category = int(conn.recv(512).decode(PROTOCOL))
        conn.sendall(game.choosingRolesMessage(names).encode(PROTOCOL))
        guesser = conn.recv(512).decode(PROTOCOL)
        game.setRolesAndCategory(names,category, guesser)
        game.cont = True
    else:
        while not game.cont:                                                # The second client must wait until the host prepares the game Category and chooses the Guesser
            pass

    conn.sendall(game.choosingObjectMessage(names, p).encode(PROTOCOL))
    time.sleep(2)
    if name == game.currentChooser:
        object = conn.recv(512).decode(PROTOCOL)
        game.setObject(object)
        game.startGame = True
    else:
        while not game.startGame:
            pass

    time.sleep(1)

    ############################## THE GAME STARTS ###################################
    
    conn.sendall((Guesser+str(counter)).encode(PROTOCOL))                     # We send the Guesser letter cause we always start the game with a question
    
    while True:
        response = conn.recv(512).decode(PROTOCOL)            # This line is going to receive the Questions/Answers from the players
        
        if name == game.currentGuesser:
            winner = checkWinner(counter, response)                # Function that checks if there is a winner everytime it receives a response from the GUESSER
            if not winner:
                print(f"{counter} {name}: {response}")
                sendToOtherPlayer(conn, response)                       # We forward the Question/Answer to the other player
                time.sleep(1)
                sendTurn(conn,p)
                counter +=1
            elif winner == name:
                winnerMessage = f"Game Over, you guessed the object! ----> '{game.secretObject}'"
                nonWinnerMessage = f"Game Over, {name} guessed the object :("
                conn.sendall(winnerMessage.encode(PROTOCOL))
                players.remove(conn)
                sendToOtherPlayer(conn, nonWinnerMessage)
                break
            else:
                winnerMessage = f"Game Over, {game.currentGuesser} didn't guessed the object, you won! "
                nonWinnerMessage = f"Game Over, you didn't guessed the object -----> {game.secretObject}"
                conn.sendall(nonWinnerMessage.encode(PROTOCOL))
                players.remove(conn)
                sendToOtherPlayer(conn, winnerMessage)
                break    
        else:
            print(f"{counter} {name}: {response}")
            if len(players) > 1:
                sendToOtherPlayer(conn, response)                       # We forward the Question/Answer to the other player
                time.sleep(1)
                sendTurn(conn,p)                                       # We send the turn to the client, we send a 'G' or 'C'
            else:
                break
    conn.close()

##################### CLIENTS CONNECTIONS #####################
p = 0
while p < 2:
    playerConnection, addr = s.accept()
    print(f"Connection {p}, Connected to: {addr}")
    players.append(playerConnection)
    if p == 0:
        game = Game()
    t1 = threading.Thread(target=handle_client, args=(playerConnection, p))
    t1.start ()
    p+=1
s.close()

###############################################################

def checkWinner(number, response):
    if game.secretObject.upper() == response.upper():
        return game.currentGuesser
    elif number == game.possibleQuestions[game.currentCategory]:
        return game.currentChooser
    else:
        return None

def checkResponse(conn):
    response = conn.recv(512).decode(PROTOCOL)
    if response.upper() == game.secretObject.upper():
        return None
    return response


