import socket
import os
import time

PROTOCOL = "utf-8"
SERVER = 'localhost'
PORT = 9000

DIVISION = "--------------------------------------------------------------------------------"

def cleanTerminal():
    os.system('cls')

def makeMove(role, numQuestion):
    #while True:
    if role == 'G':
        client.sendall(input(f"{DIVISION}\nQuestion {numQuestion}\nType a question: ").encode(PROTOCOL))
        response = client.recv(512).decode(PROTOCOL)
        print(f"{response}\n")
    else:
        client.sendall(input(f"{DIVISION}\nAnswer {numQuestion}\nType your answer: ").encode(PROTOCOL))
        response = client.recv(512).decode(PROTOCOL)
        print(f"\n{response}")
        

    if "Game Over" in response:
        return True
    return None

        

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

play = True
role = None

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


print(client.recv(512).decode(PROTOCOL))                    # Host receives the list of categories and the other player receives a waiting message
if numberOfPlayer == 0:
    client.sendall(input(">> ").encode(PROTOCOL))
    print(f"{client.recv(512).decode(PROTOCOL)}")
    guesser = input(">> ")
    client.sendall(guesser.encode(PROTOCOL))
    
role = client.recv(512).decode(PROTOCOL)
cleanTerminal()
print(role[1:])
role = role[0]


if role == 'C':
    client.sendall(input(">> ").encode(PROTOCOL))
else:
    print("Waiting for the CHOOSER to type the object...\n")

######################### THE GAME STARTS #########################
while True:
    currentTurn = client.recv(512).decode(PROTOCOL)
    numQuestion = currentTurn[1]
    if currentTurn[0] == role:
        move = makeMove(role, numQuestion)
        if move:
            break
    else:
        print("Waiting for the question...\n")
        response = client.recv(512).decode(PROTOCOL)
        print(f"{response}")
        if "Game over" in response:
            break
client.close()




