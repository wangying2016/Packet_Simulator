"""
Client side
Author: Wang Ying
Last modified: May 21 2019
"""
from socket import socket, AF_INET, SOCK_STREAM

# Create socket
tcpClientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to server
serAddr = ('127.0.0.1', 9999)
tcpClientSocket.connect(serAddr)

while True:

    # Prompt input
    sendData = input("send:")

    if len(sendData) > 0:
        tcpClientSocket.send(bytes(sendData.encode('utf-8')))
    else:
        break

    # Receive server data
    recvData = tcpClientSocket.recv(1024)
    print('recv:', recvData)

# Close socket
tcpClientSocket.close()