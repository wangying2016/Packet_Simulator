"""
Server side, long connection
Author: Wang Ying
Last modified: May 21 2019
"""
from socket import socket, AF_INET, SOCK_STREAM

# Create socket
tcpSerSocket = socket(AF_INET, SOCK_STREAM)

# Bind ip & port
address = ('127.0.0.1', 9999)
tcpSerSocket.bind(address)

# Begin listen
tcpSerSocket.listen(5)

newSocket, clientAddr = tcpSerSocket.accept()

while True:
    # Receive client data
    recvData = newSocket.recv(1024)
    # if data length is 0, because client close the connect
    if len(recvData) > 0:
        print('recv:', recvData)
    else:
        break

# Close the client socket
newSocket.close()

# Stop listen
tcpSerSocket.close()
