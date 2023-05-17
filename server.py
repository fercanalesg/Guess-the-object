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
        print("LOCKED")
        #lock.acquire()
        category = int(conn.recv(512).decode(PROTOCOL))
        print(f"Player {p} says: {category}")
        conn.sendall(game.choosingRolesMessage(names).encode(PROTOCOL))
        guesser = conn.recv(512).decode(PROTOCOL)
        game.setRolesAndCategory(names,category, guesser)
        game.cont = True
        #lock.release()
        print("REALEASED")
    else:
        while not game.cont:                                                # The second client must wait until the host prepares the game Category and chooses the Guesser
            #print(f"{p} inside")
            pass

    conn.sendall(game.choosingObjectMessage(names, p).encode(PROTOCOL))
    time.sleep(2)
    if names[p] == game.currentChooser:
        print(f"{p} LOCKED")
        #lock.acquire()
        object = conn.recv(512).decode(PROTOCOL)
        game.setObject(object)
        game.startGame = True
    else:
        while not game.startGame:
            pass

    time.sleep(1)
    conn.sendall(Guesser.encode(PROTOCOL))                     # We send the Guesser letter cause we always start the game with a question
    
    while True:
        response = conn.recv(512).decode(PROTOCOL)
        if objectGuessed(response):
            break

        print(f"{p} {response}")
        sendToOtherPlayer(conn, p, response)
        time.sleep(1)
        sendTurn(conn,p)







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


