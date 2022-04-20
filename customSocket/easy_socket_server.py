import socket as s
import sys
import threading as th

class easy_socket():
    def __init__(self):
        self.isconneced = False
        self.data = None


    def connect(self, port):
        self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        try:
            self.server_socket.bind((s.gethostbyname(s.gethostname()), self.port))
            self.server_socket.listen(1)
            self.client_socket, self.client_addr = self.server_socket.accept()
            self.isconneced = True
            th.Thread(target=self._waitForAnswer).start()
            return True
        except:
            return False

    def send(self, string):
        if self.isconneced:
            sys.exit("Connect first!")
        self.client_socket.send(bytes(string, "utf8"))

    def waitForAnswer(self):
        while True:
            if self.data != None:
                self.tempData = self.data
                self.data = None
                return self.tempData

    def _waitForAnswer(self):
        if self.isconneced:
            sys.exit("Connect first!")
        while True:
            self.raw_data = self.client_socket.recv(1024)
            self.raw_data = str(self.raw_data, "utf8")
            if self.raw_data != "":
                self.data = self.raw_data