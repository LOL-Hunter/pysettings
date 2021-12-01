import pyfiglet as py
import termcolor as c
import colorama as co
import random as r
import time as t
from enum import Enum
import os
co.init(autoreset=True)

class Color(Enum):
    GREY = "grey"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"
    BLACK = None


class TextColor:
    @staticmethod
    def get(text, col=Color.BLACK):
        if hasattr(col, "value"): col = col.value
        return c.colored(text, color=col)
    @staticmethod
    def print(text, col=Color.BLACK):
        if hasattr(col, "value"): col = col.value
        print(c.colored(text, color=col))
class Title:
    def __init__(self, font="big"):
        self._title = py.Figlet(font=font)
    def _outline(self, text, char):
        length = len(text.split("\n")[0]) +2
        textN = str(length*char)+"\n"
        for i in text.split("\n"):
            if i!= "":
                textN+= char + i + char +"\n"
        return textN + length*char+"\n"
    def print(self, text, col=Color.BLACK):
        TextColor.print(self._title.renderText(text), col)
    def get(self, text, outLine=""):
        if outLine != "":
            return self._outline(self._title.renderText(text), outLine)
        return self._title.renderText(text)
class MsgText:
    @staticmethod
    def info(msg):
        TextColor().print(t.strftime("[INFO-%H:%M:%S]: ")+str(msg), Color.GREEN.value)
    @staticmethod
    def warning(msg):
        TextColor().print(t.strftime("[WARNING-%H:%M:%S]: ")+str(msg), Color.YELLOW.value)
    @staticmethod
    def help(msg):
        TextColor().print("[HELP]: " + str(msg), Color.YELLOW.value)
    @staticmethod
    def error(msg, exit_=False):
        TextColor().print(t.strftime("[ERROR-%H:%M:%S]: ") + str(msg), Color.RED.value)
        if exit_: os._exit(0)
        
            

if __name__ == '__main__':
    Title().print("Test", Color.BLUE)
