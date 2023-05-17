import socket
import os
import time

PROTOCOL = "utf-8"
SERVER = 'localhost'
PORT = 9000



def cleanTerminal():
    os.system('cls')

def makeMove(role):
    while True:
        if role == 'G':
            client.sendall(input("Type a question: ").encode(PROTOCOL))
        else:
            client.sendall(input("Type your answer: ").encode(PROTOCOL))

        response = client.recv(512).decode(PROTOCOL)
        print(response)

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
#print(role)

if role == 'C':
    client.sendall(input(">> ").encode(PROTOCOL))
else:
    print("Waiting for the CHOOSER to type the object...")

while True:
    currentTurn = client.recv(512).decode(PROTOCOL)
    #cleanTerminal()
    print(currentTurn)
    if currentTurn[0] == role:
        makeMove(role)
    else:
        response = client.recv(512).decode(PROTOCOL)
        print(f"R: {response}")




