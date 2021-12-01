import os
import platform
from plyer import wifi, camera, battery, email, notification
from pysettings.text import MsgText
from wifi import Cell, Scheme

class Camera:
    @staticmethod
    def takePicture(path):
        return camera.take_picture(path)

class Battery:
    @staticmethod
    def hasBattery():
        return battery.get_state()["percentage"] != -1
    @staticmethod
    def getPercentage():
        return battery.get_state()["percentage"]
    @staticmethod
    def isCharging():
        return battery.get_state()["isCharging"]

class Email:
    @staticmethod
    def openNewMail(to=None, subject=None, text=None):
        email.send(to, subject, text)
    @staticmethod
    def sendEmail():
        pass

class Notification:
    @staticmethod
    def notify(title="", msg="", appName="", showTime=10, ticker=""):
        notification.notify(title=title, message =msg, app_name =appName, app_icon ="", timeout=showTime, ticker=ticker)

class Wifi:
    pass

class SystemInfo:
    @staticmethod
    def getUserName():
        return os.getlogin()
    @staticmethod
    def getOperatingSys():
        return platform.system()



if __name__ == '__main__':
   pass