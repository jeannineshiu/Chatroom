#!/usr/bin/env python
# coding: utf-8

# In[1]:



from PyQt5 import QtGui
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
import sys
import socket
from threading import Thread
from clientUI import Ui_Form


# In[2]:


class AppWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.sendbt.clicked.connect(self.on_click)
            
        self.show()

        client = socket.socket()
        client.connect(('127.0.0.1', 8002))
        self.client = client
        self.begin_thread()


    def on_click(self):
        print("PyQt5 button click")
        self.send_msg()
        self.ui.edtext.clear()
        
    def send(self):
        self.ui.sendbt.clicked.connect(self.on_click)

    def begin_thread(self):
        Thread(target=self.send).start()
        Thread(target=self.recv_msg).start()

    def send_msg(self):
        msg = self.ui.edtext.toPlainText()
        print(msg)
        self.client.send(msg.encode())
        if (msg.upper() == "QUIT"):
            self.client.close()
        self.ui.edtext.clear()

    def recv_msg(self):
        while 1:
            try:
                data = self.client.recv(1024).decode()
                data = data + "\n"
                self.ui.textbrowid.append(data)
            except:
                exit()

    def closeEvent(self, QCloseEvent):
        self.client.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)  
    MainWindow = AppWindow()
    MainWindow.show()
    sys.exit(app.exec_())  

