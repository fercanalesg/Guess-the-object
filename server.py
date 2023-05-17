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
counter = 0

def sendToBothPlayers(message):
    for player in players:
        player.sendall(message.encode(PROTOCOL))

def sendToOtherPlayer(conn, p, message):
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
            player.sendall(nextTurn.encode(PROTOCOL))

def handle_client(conn, p): 
    global counter
    name = conn.recv(512).decode(PROTOCOL)                                   # We recover the clients name
    names.insert(p, name)
    print(f"{name} is player {p}")
    conn.sendall(str(p).encode(PROTOCOL))                                     # We send the number of player
    conn.recv(512).decode(PROTOCOL)                                           # We just receive the approval of connection
    conn.sendall(game.introducingMessage(p, names).encode(PROTOCOL))          # We send the introducing message
    conn.recv(512).decode(PROTOCOL)
############################################################
    
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
    if names[p] == game.currentChooser:
        object = conn.recv(512).decode(PROTOCOL)
        game.setObject(object)
        game.startGame = True
    else:
        while not game.startGame:
            pass

    time.sleep(1)
    currentPlayer = game.currentGuesser

    conn.sendall(Guesser.encode(PROTOCOL))                     # We send the Guesser letter cause we always start the game with a question
    
    response = ''
    while response != game.secretObject and counter < game.possibleQuestions[game.currentCategory]:
        print(f"{p} ENTERED")
        response = conn.recv(512).decode(PROTOCOL)
        if objectGuessed(response):
            break
        if names[p] == game.currentGuesser:
            counter +=1
            print(f"{counter} {names[p]}: {response}")
        else:
            print(f"{names[p]}: {response}")

        sendToOtherPlayer(conn, p, response)
        time.sleep(1)
        sendTurn(conn,p)

    print("MAMO no mas preguntas bro")
    conn.close()


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

def objectGuessed(response):
    if response.upper() == game.secretObject.upper():
        return True
    return None

def checkResponse(conn):
    response = conn.recv(512).decode(PROTOCOL)
    if response.upper() == game.secretObject.upper():
        return None
    return response


