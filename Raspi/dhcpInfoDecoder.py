import os, sys, subprocess as s
import threading as th
import time as t

WORKING_DIR = os.getcwd()

class DHCPInfoParser:
    def __init__(self):
        self.out = s.check_output(["iw", "dev", "wlan0", "station", "dump"]).decode().replace("\t", "").replace(" ", "").replace("seconds", "")
        self.connections = []
        if self.out != "":
            self.decode()

    def decode(self):
        self.connections = []
        for i in self.out.split("Station")[1:]:
            d = {"address":i.split("(")[0]}
            i = i[len(d["address"]):]
            for j in i.split("\n")[1:]:
                if j != "": d[j.split(":")[0]] = j.split(":")[1]
            if len(d.keys()) == 18: self.connections.append(d)
    @staticmethod
    def getConnections():
        return DHCPInfoParser().connections
class ClientConnectionListener:
    DELAY = 0.4
    def __init__(self, hook=None):
        self.eventFunc = hook
        th.Thread(target=self._listen, daemon=True).start()
    def _listen(self):
        self.savedData = DHCPInfoParser.getConnections()
        while True:
            data = DHCPInfoParser.getConnections()
            t.sleep(ClientConnectionListener.DELAY)
            if len(self.savedData) < len(data):
                self.eventFunc(data[[int(i["connectedtime"]) for i in data].index(min([int(i["connectedtime"]) for i in data]))]["address"])
            else:
                for con in data:
                    for savcon in self.savedData:
                        if con["address"] == savcon["address"] and int(con["connectedtime"]) < int(savcon["connectedtime"]):
                            self.eventFunc(con["address"])
            self.savedData = data.copy()

class Wlan0Config:
    WLAN_CONFIG_PATH=r"/etc/dnsmasq.d/090_wlan0.conf"
    TEMP_WLAN_CONFIG_PATH = os.path.join(WORKING_DIR, "package", "temp.txt")
    @staticmethod
    def read():
        if not os.path.exists(Wlan0Config.WLAN_CONFIG_PATH):
            return {}
        data = {}
        file = open(Wlan0Config.WLAN_CONFIG_PATH, "r")
        for line in file:
            if line.startswith("dhcp-host"):
                data[line.split("=")[1].split(",")[0]] = line.split("=")[1].split(",")[1].replace("\n", "")
        file.close()
        return data
    @staticmethod
    def setInternConfigPath(path):
        Wlan0Config.TEMP_WLAN_CONFIG_PATH = path
    @staticmethod
    def getIpAddresses():
        a = list(Wlan0Config.read().values())
        a.sort()
        return a
    @staticmethod
    def write(data):
        sorce = open(Wlan0Config.WLAN_CONFIG_PATH, "r")
        text=""
        for line in sorce:
            if not line.startswith("dhcp-host"):
                text+=line
        sorce.close()
        temp = open(Wlan0Config.TEMP_WLAN_CONFIG_PATH, "w")
        if data is not None:
            for i in data.keys():
                text+="dhcp-host="+i+","+data[i]+"\n"
        temp.write(text.replace("\"", "\'"))
        temp.close()
        os.system("sudo rm "+Wlan0Config.WLAN_CONFIG_PATH)
        os.system("sudo cp "+Wlan0Config.TEMP_WLAN_CONFIG_PATH+" "+Wlan0Config.WLAN_CONFIG_PATH)



if __name__ == "__main__":
   print(Wlan0Config.write({"mac":"0.0.02"}))
