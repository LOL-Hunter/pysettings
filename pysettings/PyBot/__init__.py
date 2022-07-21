import mss
import pyautogui as py
from pysettings.geometry import Location2D
import pysettings.key_Listener as l
import pysettings.tk as tk
import threading as th
import time as t
import pygame
import ctypes
pygame.init()
def getPixelColor(loc:Location2D):
    return py.pixel(loc.getX(), loc.getY())

def sleep(f):
    t.sleep(f)
def getMouseLocation_():
    p = py.position()
    return Location2D(p.x, p.y)
def getMouseLocation():
    x, y=pygame.mouse.get_pos()
    return Location2D(x, y)
class Listener(l.Listener):
    pass

class ScreenImage:
    pass

class Mouse:
    @staticmethod
    def leftClick(loc: Location2D=None):
        if loc!= None:
            py.moveTo(x=loc.getX(), y=loc.getY())
        py.mouseDown(button=py.LEFT)
        sleep(0.1)
        py.mouseUp(button=py.LEFT)
    @staticmethod
    def rightClick(loc: Location2D):
        py.moveTo(x=loc.getX(), y=loc.getY())
        py.mouseDown(button=py.RIGHT)
        sleep(0.1)
        py.mouseUp(button=py.RIGHT)
    @staticmethod
    def middleClick(loc: Location2D):
        py.moveTo(x=loc.getX(), y=loc.getY())
        py.mouseDown(button=py.MIDDLE)
        sleep(0.1)
        py.mouseUp(button=py.MIDDLE)
    @staticmethod
    def moveTo(loc:Location2D, time=0):
        py.moveTo(x=loc.getX(), y=loc.getY(), duration=time)

class System:
    @staticmethod
    def getScreenSize():
        return Location2D(py.size().width, py.size().height)

class Info:
    def __init__(self):
        pass
    def showGUI(self):
        self.master = tk.Tk()

        th.Thread(target=self.update).start()
        self.master.mainloop()
    def update(self):
        t.sleep(0.5)
        while True:
            self.master.update()
            py.mouseInfo()


if __name__ == '__main__':
    Info().showGUI()