"""
Client side, short connection
Author: Wang Ying
Last modified: May 21 2019
"""
from socket import socket, AF_INET, SOCK_STREAM


while True:

    # Prompt input
    sendData = input("send:")

    # Create socket
    tcpClientSocket = socket(AF_INET, SOCK_STREAM)

    # Connect to server
    serAddr = ('127.0.0.1', 9999)
    tcpClientSocket.connect(serAddr)

    # Send data
    tcpClientSocket.send(bytes(sendData.encode('utf-8')))

    # Close connection
    tcpClientSocket.close()

    # Out condition
    if len(sendData) == 0:
        break


