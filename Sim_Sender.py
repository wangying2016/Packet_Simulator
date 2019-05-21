"""
Packet simulator client
Author: Wang Ying
Last modified: May 21 2019
Intro:
-> packet definition
000023|0001|I send 0001
6 bit total message's length|4 bit identification code|message content
-> identification code
0000   general request & response
0001   test 0001 greeting
0002   test 0002 greeting
others 0000 requtest & response
"""
from tkinter import Tk, Text, BOTH, X, Y, N, LEFT, RIGHT, messagebox, END, INSERT
from tkinter.ttk import Frame, Label, Entry, Button
from tkinter import scrolledtext, filedialog
from socket import socket, AF_INET, SOCK_STREAM
import threading
import time


class Maker:
    """
    Packet generate class.
    """
    def __init__(self):
        self.index = ''
        self.content = ''
        self.msg = ''

    def get_msg(self, index, content):
        self.index = index
        self.content = content
        length = 6 + 4 + 2 + len(content)
        self.msg = '{:0>6}'.format(length) + '|' + index + '|' + content
        return self.msg

    def get_index(self):
        return self.index

    def get_content(self):
        return self.content


class Reader:
    """
    Packet analysis class.
    """
    def __init__(self, msg):
        self.msg = msg
        self.index = msg[7:11]
        self.content = msg[12:]

    def get_index(self):
        return self.index

    def get_content(self):
        return self.content


class Server:
    """
    Listen message from server.
    """
    def __init__(self):
        # Create socket
        self.tcp_server_socekt = socket(AF_INET, SOCK_STREAM)

        # Bind IP & port
        self.server_address = (client_ip, client_port)
        self.tcp_server_socekt.bind(self.server_address)

        # Begin listen
        self.tcp_server_socekt.listen(1)
        print('start listen')

        # Server long connection, client short connection
        while True:
            # Listen for connection
            new_socket, client_address = self.tcp_server_socekt.accept()

            # Receive client data
            recv_data = str(new_socket.recv(1024), encoding='utf-8')
            print(recv_data)

            # if data length is 0, it is because client close the connect
            if len(recv_data) > 0:
                reader = Reader(recv_data)
                index = reader.get_index()
                content = reader.get_content()
                log = 'index = [%s]\ncontent = [%s]\ndata = [%s]\n' % (index, content, recv_data)
                app.add_log('recv data', log)
            else:
                print('recv data = 0\n')

            # Close the client socket
            new_socket.close()

        # Stop listen
        self.tcpSerSocket.close()


class Client:
    """
    Send message to server.
    """
    def __init__(self, data):
        # Create socket
        self.tcp_client_socket = socket(AF_INET, SOCK_STREAM)

        # Bind ip & port
        self.server_address = (server_ip, server_port)

        # Connect to server
        self.tcp_client_socket.connect(self.server_address)

        # Send data
        self.tcp_client_socket.send(bytes(data.encode("utf-8")))

        # Close connect
        self.tcp_client_socket.close()

        # Add log
        data = 'data = [%s]' % data
        app.add_log('send data', data)


class GUI(Frame):
    """
    GUI with tkinter.
    """
    def __init__(self):
        super().__init__()
        # Instance variable
        self.frame1 = ''
        self.frame2 = ''
        self.frame3 = ''
        self.frame4 = ''
        self.frame5 = ''
        self.entry = ''
        self.txt = ''
        self.log = ''

        # Init ui
        self.init_ui()

        # Begin listen
        t = threading.Thread(target=network)
        t.setDaemon(True)
        t.start()

    def init_ui(self):
        self.master.title("报文模拟器")
        self.pack(fill=BOTH, expand=True)

        self.frame1 = Frame(self)
        self.frame1.pack(fill=X, expand=True)

        lbl1 = Label(self.frame1, text="识别代码", width=10)
        lbl1.pack(side=LEFT, padx=5, pady=5)

        self.entry = Entry(self.frame1)
        self.entry.pack(fill=X, padx=5, expand=True)

        self.frame2 = Frame(self)
        self.frame2.pack(fill=X, expand=True)

        lbl2 = Label(self.frame2, text="报文内容", width=10)
        lbl2.pack(side=LEFT, anchor=N, padx=5, pady=5)

        self.txt = Text(self.frame2, height=10)
        self.txt.pack(fill=X, pady=5, padx=5, expand=True)

        self.frame3 = Frame(self)
        self.frame3.pack(fill=X, expand=True)

        button1 = Button(self.frame3, text="打开本地", command=self.open_local)
        button1.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)

        button2 = Button(self.frame3, text="保存本地", command=self.save_local)
        button2.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)

        button3 = Button(self.frame3, text="发送报文", command=self.send_msg)
        button3.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)

        self.frame4 = Frame(self)
        self.frame4.pack(fill=X, expand=True)

        lbl3 = Label(self.frame4, text='日志监控')
        lbl3.pack(side=LEFT, padx=5, pady=5)

        self.frame5 = Frame(self)
        self.frame5.pack(fill=BOTH, expand=True)

        self.log = scrolledtext.ScrolledText(self.frame5, height=55, width=150)
        self.log.pack(side=LEFT, pady=5, padx=5, expand=True)
        self.log.focus_set()

        self.add_log('packet simulator', 'start listen')

    def add_log(self, title, msg):
        tm = time.localtime(time.time())
        fmt_msg = '%s-%s-%s %s:%s:%s %s\n%s\n\n' % (tm.tm_year,
                                                    '{:0>2}'.format(tm.tm_mon),
                                                    tm.tm_mday,
                                                    '{:0>2}'.format(tm.tm_hour),
                                                    '{:0>2}'.format(tm.tm_min),
                                                    '{:0>2}'.format(tm.tm_sec),
                                                    title,
                                                    msg)
        self.log.insert(INSERT, fmt_msg)
        self.log.focus_set()
        self.log.yview_moveto(1)

    def send_msg(self):
        # Get parameter
        argv1 = self.entry.get().strip()
        argv2 = self.txt.get('1.0', END).strip().replace('\n', '')
        if len(argv1) != 4:
            messagebox.showerror('错误', '请输入 4 位识别代码')
            return
        print('argv1 = [%s], argv2 = [%s]' % (argv1, argv2))

        # Make message
        maker = Maker()
        msg = maker.get_msg(argv1, argv2)
        print('send data: \n[%s]\n' % msg)

        # Send Data
        client = Client(msg)

    def open_local(self):

        ftypes = [('Merch simulator message format', '*.ms'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes=ftypes)
        filename = dlg.show()

        if filename != '':
            text = self.read_file(filename)
            self.txt.insert(INSERT, text)

    def save_local(self):
        ftypes = [('Packet simulator format', '*.ms'), ('All files', '*')]
        filename = filedialog.asksaveasfilename(filetypes=ftypes)

        if filename != '':
            text = self.txt.get('1.0', END).strip().replace('\n', '')
            self.write_file(filename, text)

    def read_file(self, filename):

        with open(filename, 'r') as f:
            text = f.read()

        return text

    def write_file(self, filename, text):

        with open(filename, 'w') as f:
            f.write(text)


def network():
    server = Server()


if __name__ == '__main__':
    # IP & port
    server_ip = '127.0.0.1'
    server_port = 9999
    client_ip = '127.0.0.1'
    client_port = 8888

    # Gui
    root = Tk()
    app = GUI()
    w = int(app.master.winfo_screenwidth() / 2)
    h = int(app.master.winfo_screenheight())
    # Half screen
    # root.geometry("%sx%s+0+0" % (w, h))
    root.geometry("350x600+300+300")
    root.mainloop()
