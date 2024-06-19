import os
import time as t
from enum import Enum
import colorama as co
import pyfiglet as py
import termcolor as c

co.init(autoreset=True)

class Log:
    _configActive = False
    _path = ""
    _config = None
    @staticmethod
    def logMsg(path):
        # could be that the file doesn't exists
        _config = open(path, "a")
        Log._configActive = True

    @staticmethod
    def save():
        Log._config.close()

    @staticmethod
    def _write(msg):
        if Log._configActive:
            Log._config.write(msg+"\n")
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
    def _strf(text):
        """
                §D: DEFAULT
                §W: WHITE
                §B: BLACK

                §r: RED
                §g: GREEN
                §b: BLUE
                §c: CYAN
                §y: YELLOW
                §m: MAGENTA

                @param text:
                @return:
                """

        colors = {'§W':Color.WHITE.value,
                  '§B':Color.BLACK.value,
                  '§r':Color.RED.value,
                  '§g':Color.GREEN.value,
                  '§b':Color.BLUE.value,
                  '§c':Color.CYAN.value,
                  '§y':Color.YELLOW.value,
                  '§m':Color.MAGENTA.value}
        text = text.replace("§INFO", t.strftime("§g[INFO-%H:%M:%S]: "))
        text = text.replace("§ERROR", t.strftime("§r[ERROR-%H:%M:%S]: "))
        text = text.replace("§WARN", t.strftime("§y[WARNING-%H:%M:%S]: "))

        fmt_str = "\033[%dm"
        for k, v in zip(colors.keys(), colors.values()):
            while k in text:
                text = text.replace(k, fmt_str % c.COLORS[v])
        return text
    @staticmethod
    def getStrf(text):
        return TextColor._strf(text)
    @staticmethod
    def printStrf(text):
        print(TextColor._strf(text))
    @staticmethod
    def get(text, col=Color.BLACK):
        if hasattr(col, "value"): col = col.value
        return c.colored(text, color=col)
    @staticmethod
    def print(text, col=Color.BLACK, end="\n"):
        if hasattr(col, "value"): col = col.value
        print(c.colored(text, color=col), end=end)
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
    def info(msg, strf=False):
        _text = t.strftime("[INFO-%H:%M:%S]: ")+str(msg)
        Log._write(_text)
        if not strf: TextColor.print(_text, Color.GREEN)
        else: TextColor.printStrf("§g"+_text)
    @staticmethod
    def warning(msg):
        _text = t.strftime("[WARNING-%H:%M:%S]: ")+str(msg)
        Log._write(_text)
        TextColor.print(_text, Color.YELLOW)
    @staticmethod
    def help(msg):
        TextColor.print("[HELP]: " + str(msg), Color.YELLOW)
    @staticmethod
    def error(msg, exit_=False):
        _text = t.strftime("[ERROR-%H:%M:%S]: ") + str(msg)
        Log._write(_text)
        TextColor.print(_text, Color.RED)
        if exit_:
            Log._write("="*5+"SystemExit by MsgText-error"+"="*5)
            Log.save()
            os._exit(0)


if __name__ == '__main__':
    TextColor.printStrf("123§rHallo§gWelt")
