#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
from threading import Thread

import time


class server:
    def __init__(self):
        server = socket.socket()
        server.bind(('127.0.0.1', 8002))
        server.listen(5)
        self.server = server
        self.li = []  # list of clients
        self.di = {}  # tuple of client's name and its IP address
        self.get_con()

    def get_con(self):  # a loop for waiting connections from clients
        while 1:
            con, addr = self.server.accept()
            data = 'Welcome! Please type your name~ '
            con.send(data.encode())  # inform the client
            Thread(target=self.get_msg, args=(con, self.li, self.di, addr)).start()  # launch a thread
            self.li.append(con)  # save the client's info

    def get_msg(self, con, li, di, addr):
        name = con.recv(1024).decode()  # receive client's name
        di[addr] = name  # add to the tuple {addr,name}
        while 1:  # a loop for listening to the client
            try:
                redata = con.recv(1024).decode()
            except Exception as e:
                self.close_client(con, addr)
                break;
            if (redata.upper() == "QUIT"):
                self.close_client(con, addr)
                break;
            # print client's addr + time + what client sent on the console
            print(di[addr] + ' ' + time.strftime('%x') + ':\n' + redata)
            for i in li:  # show the content to all the clients
                i.send((di[addr] + ' ' + time.strftime('%x') + ':\n' + redata).encode())

    def close_client(self, con, addr):
        self.li.remove(con)
        # print("client:", self.li)
        con.close()
        print(self.di[addr] + " has leave")
        for k in self.li:
            k.send((self.di[addr] + " has leave").encode())


if __name__ == "__main__":
    server()

