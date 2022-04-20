import socket as s
import threading as th
import sys

conneced = False
anw = None

def connect(ip, port):
    global conneced
    clientsocket = s.socket(s.AF_INET, s.SOCK_STREAM)
    clientsocket.connect((ip, port))
    th.Thread(target=_waitForAnswer).start()
    conneced = True

def send(string):
    if conneced:
        sys.exit("Connect first!")
    self.clientsocket.send(bytes(string, "utf8"))

def _waitForAnswer():
    global anw
    if conneced:
        sys.exit("Connect first!")
    while True:
        raw_anw = str(self.clientsocket.recv(1024), "utf8")
        if raw_anw != "":
            anw = raw_anw

def waitForAnswer():
    if conneced:
        sys.exit("Connect first!")
    while True:
        if anw != None:
            return anw
