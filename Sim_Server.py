"""
Packet simulator server
Author: Wang Ying
Last modified: May 21 2019
"""
from socket import socket, AF_INET, SOCK_STREAM


class Processor:
    """
    Processing a message.
    """
    def __init__(self, msg):
        self.recv_msg = msg

        # Check receive message
        if len(self.recv_msg) < 11:
            print('Message invalid')
            self.index = '0000'
            self.content = 'invalid message'
            self.send_msg = '000027|0000|invalid messgae'
            return

        # Read message
        self.index = self.recv_msg[7:11]
        self.content = self.recv_msg[12:]

        # Write message
        if self.index == '0001':
            self.send_content = 'I received 0001'
        elif self.index == '0002':
            self.send_content = 'I received 0002'
        else:
            self.send_content = 'I cannot recognize'

        # Packet message
        length = 6 + 4 + 2 + len(self.index) + len(self.send_content)
        self.send_msg = '{:0>6}'.format(length) + '|' + self.index + '|' + self.send_content

    def get_msg(self):
        return self.send_msg


class Client:
    """
    Send message to client.
    """
    def __init__(self, data):
        # Create socket
        self.tcp_client_socket = socket(AF_INET, SOCK_STREAM)

        # Bind ip & port
        self.server_address = (client_ip, client_port)

        # Connect to client
        self.tcp_client_socket.connect(self.server_address)

        # Send data
        self.tcp_client_socket.send(bytes(data.encode("utf-8")))

        # Close connect
        self.tcp_client_socket.close()


class Server:
    """
    Listen for client.
    """
    def __init__(self):
        # Create socket
        tcp_server_socekt = socket(AF_INET, SOCK_STREAM)

        # Bind ip & port
        server_address = (server_ip, server_port)
        tcp_server_socekt.bind(server_address)

        # Begin listen
        tcp_server_socekt.listen(1)
        print('start listen\n')

        # Server long connection, client short connection
        while True:
            # Listen for client's connection
            new_socket, client_address = tcp_server_socekt.accept()

            # Receive client data
            recv_data = str(new_socket.recv(1024), encoding='utf-8')

            # if data length is 0, because client close the connect
            if len(recv_data) > 0:
                print('recv data = [%s]\n' % recv_data)
            else:
                print('recv data = 0\n')

            # Processing message
            processor = Processor(recv_data)
            send_data = processor.get_msg()
            client = Client(send_data)
            print('send data = [%s]\n' % send_data)

            # Close the client socket
            new_socket.close()

        # Stop listen
        tcp_server_socekt.close()


if __name__ == '__main__':
    server_ip = '127.0.0.1'
    server_port = 9999
    client_ip = '127.0.0.1'
    client_port = 8888
    server = Server()
