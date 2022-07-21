import socket as s
from pysettings import IndependentTimer, ID, Queue as _Queue
from pysettings.text import MsgText
import time as t
import threading as th



class Client:
    pass



class Server:
    def __init__(self, ip, port):
        """
        



        @param ip:
        @param port: The Server running on this port.
        """
        self.DEBUG = True
        self._isClosingInProgess = False
        self._isConnected = False
        self._queue = _Queue()
        # NETWORK
        self._ip = (ip, port, ID.newId(8))
        self._serverSocket = None
        self._clientSocket = None
        self._clientAddress = None

    def __str__(self):
        return str(self._ip)

    def setDebugMode(self, b:bool):
        self.DEBUG = b
        
    def getConnected(self):
        return self._isConnected

    def getClientAddress(self):
        assert self._isConnected, "Connect first to get the ClientAddress!"
        return self._clientAddress

    def onConnectionEstablished(self, func):
        pass

    def onConnectionClosed(self, func):
        pass

    def connect(self, trys=-1, waitBetween=5):
        _trys=0
        while not self._isConnected:
            self._serverSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
            try:
                self._serverSocket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
                self._serverSocket.bind(("", self._ip[1]))
                self._serverSocket.listen(1)
                self._clientSocket, self._clientAddress = self._serverSocket.accept()
                if self.DEBUG: MsgText.info("Connection established with " + str(self._ip))
                self._isConnected = True
                th.Thread(target=self._waitForAnswer).start()
                return True
            except Exception as e:
                _trys+=1
                if self.DEBUG: MsgText.error("Connection failed with " + str(self._ip) + " retrying in (5) sek...")
                t.sleep(waitBetween)
                if trys != -1 and _trys >= trys: return False


    def send(self, text_):
        if self._isConnected:
            try:
                self._clientSocket.send(bytes(text_, "utf8"))
                return True
            except Exception as e:
                if self.DEBUG: MsgText.error("Error while sending " + text_ + " " + str(e))
        else:
            if self.DEBUG: MsgText.error("Could not send " + str(text_) + "! Client " + str(self._ip) + " is not connected!")
        return False

    def getQueue(self):
        return self._queue.get()

    def _waitForAnswer(self):
        while self._isConnected:
            try:
                data = str(self._clientSocket.recv(1024), "utf8")
            except Exception as e:
                if self.DEBUG: MsgText.error("Error while waiting for answer..." + str(self._ip) + str(e))
                return
            # if not data: --> client.stop() (kein stop wenn ausgesteckt)
            # MsgText.error("Data (Empty String): "+str(type(data))+str(self.ip))#for testing
            # self._isConnected = False
            if data != "":
                self.q = t.time()
                self._queue.append(data)

    def close(self):
        if not self._isClosingInProgess and self._isConnected:
            try:
                self.isClosingInProgess = True
                self._isConnected = False
                self._serverSocket.close()
                self._clientSocket.close()
                if self.DEBUG: MsgText.warning("CONNECTION: " + str(self._ip) + " CLOSED!")
            except:
                MsgText.error("Could not close: " + str(self._ip))
        self._isClosingInProgess = False
        self._queue.clear()