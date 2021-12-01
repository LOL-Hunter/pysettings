import threading as th
import tkinter as tk
import tkinter.ttk as ttk
import time as t
import sys


class StartProgressWindow:
    def __init__(self, text="Please Wait", title="ProgressWindow"):
        self._stopAnimation = False
        self._Labeltext = text
        self._windowtitle = title
        th.Thread(target=self.__thread_window).start()

    def __animation(self):
        self._animationString = ""
        self._currTime = t.time()
        while True:
            if self._stopAnimation:
                try:
                    self._master.destroy()
                except:
                    pass
                return
            else:
                t.sleep(0.1)

                self._currTime = t.time()
                self._label["value"] += 10

    def __thread_window(self):
        self._master = tk.Tk()
        self._master.protocol("WM_DELETE_WINDOW", 0)
        self._master.title(self._windowtitle)

        #self._master.minsize(200, 100)

        self._spacelabel12 = tk.Label(self._master)
        self._spacelabel12["text"] = "      "
        self._spacelabel12.grid(row=0, column=0)

        self._spacelabel1 = tk.Label(self._master)
        self._spacelabel1["text"] = self._Labeltext
        self._spacelabel1.grid(row=1, column = 1)

        self._label = ttk.Progressbar(self._master)
        self._label["value"] = 0
        self._label["mode"] = "indeterminate"
        self._label.grid(row=2, column = 1)

        self._spacelabel2 = tk.Label(self._master)
        self._spacelabel2["text"] = ""
        self._spacelabel2.grid(row=3, column=1)

        self._spacelabel23 = tk.Label(self._master)
        self._spacelabel23["text"] = "      "
        self._spacelabel23.grid(row=4, column=2)

        th.Thread(target=self.__animation).start()
        self._master.mainloop()

        return

    def stop(self):
        self._stopAnimation = True
class StartProgressBar:
    def __init__(self, text="",allvalues = 100, title="ProgressWindow", close = True):
        self._value = 0
        self.info = ""
        self._exit = False
        self._close = close
        self._finishProgress = False
        self._allvalues = allvalues
        if allvalues <= 0:
            sys.exit("all values must be highter than 0")
        self._windowCreated = True
        self._LabeltextBar = text
        self._windowtitleBar = title
        th.Thread(target=self.__thread_windowBar).start()
        while self._windowCreated:
            pass
        t.sleep(0.1)

    def __animationBar(self):
        self._startTime = t.time()
        self._animationString = ""
        self._currTime=t.time()
        self._tempTime = t.time()
        self._tempCount = 0
        while True:
            self._prog = int(((self._value/self._allvalues)*100)/2)
            self._empyprog =50-self._prog
            if self._tempTime+1 <= t.time():
                self._labelBarPS["text"] = str(self._tempCount) + "/Sek"
                self._tempTime = t.time()
                self._tempCount = 0
            self._labelBar["value"] = self._prog*2
            self._labelBarProg["text"] = str(round((self._value/self._allvalues)*100, 2))+" %"
            self._labelBarTotal["text"] = "["+str(self._value)+"|"+str(self._allvalues)+"]"
            self._master.update()
            if self._exit:
                self._finishProgress = True
                try:
                    self._master.destroy()
                except:
                    pass
                return
            elif self._allvalues <= self._value and self._close:
                self._finishProgress = True
                try:
                    self._master.destroy()
                except:
                    pass
                return

    def __thread_windowBar(self):
        self._master = tk.Tk()
        self._master.protocol("WM_DELETE_WINDOW",0)
        self._master.title(self._windowtitleBar)
        self._master.minsize(200, 100)
        self._spacelabel1 = tk.Label(self._master)
        self._spacelabel1["text"] = self._LabeltextBar
        self._spacelabel1.grid(row = 1, column=1)

        self._sp2 = tk.Label(self._master)
        self._sp2["text"] = "           "
        self._sp2["font"] = ("arial", 15)
        self._sp2.grid(row = 2, column= 0)

        self._sp3 = tk.Label(self._master)
        self._sp3["text"] = "           "
        self._sp3["font"] = ("arial", 15)
        self._sp3.grid(row=2, column=2)

        self._labelBar = ttk.Progressbar(self._master)
        self._labelBar["length"] = 200
        #self._labelBar["mode"] = 'indeterminate'
        #self._labelBar["font"] = ("arial", 15)
        self._labelBar.grid(row=2, column=1)

        self._labelBarInf = tk.Label(self._master)
        self._labelBarInf["text"] = self.info
        self._labelBarInf.grid(row=3, column=1)

        self._labelBarProg = tk.Label(self._master)
        self._labelBarProg["text"] = ""
        self._labelBarProg.grid(row=4, column=1)

        self._labelBarTotal = tk.Label(self._master)
        self._labelBarTotal["text"] = ""
        self._labelBarTotal.grid(row=5, column=1)

        self._labelBarPS = tk.Label(self._master)
        self._labelBarPS["text"] = "0/Sek"
        self._labelBarPS.grid(row=6, column=1)

        self._spacelabel2 = tk.Label(self._master)
        self._spacelabel2["text"] = ""
        self._spacelabel2.grid(row=7, column=1)

        th.Thread(target=self.__animationBar).start()
        self._windowCreated = False
        self._master.mainloop()
        return

    def addValue(self, info = ""):
        if self._value <= self._allvalues:
            self._labelBarInf["text"] = info
            self._value += 1
            self._tempCount += 1

    def reset(self):
        if not self._close:
            self._value = 0
            self._finishProgress = False
            self._startTime = t.time()
            self._animationString = ""
            self._currTime = t.time()
            self._tempTime = t.time()
            self._tempCount = 0

    def exit(self):
        if not self._close:
            self._exit = True

    def getTime(self):
        if self._finishProgress:
            return t.time() - self._startTime
        else:
            return None

    def isBarFull(self):
        if self._value == self._allvalues:
            return False
        else:
            return True
class _Progress:
    def __init__(self):
        pass

    def _updateBar(self):
        self._startTime = t.time()
        self._animationString = ""
        self._currTime=t.time()
        self._tempTime = t.time()
        self._tempCount = 0
        while True:
            self._prog = int(((self._value/self._allvalues)*100)/2)
            self._empyprog =50-self._prog
            if self._tempTime+1 <= t.time():
                self._labelBarPS["text"] = str(self._tempCount) + "/Sek"
                self._tempTime = t.time()
                self._tempCount = 0
            self._labelBar["text"] = "["+"I"*self._prog+"."*self._empyprog+"]"
            self._labelBarProg["text"] = str(round((self._value/self._allvalues)*100, 2))+" %"
            self._labelBarTotal["text"] = "["+str(self._value)+"|"+str(self._allvalues)+"]"
            self._master.update()
            if self._allvalues == self._value:
                self._finishProgress = True
                try:
                    self._master.destroy()
                except:
                    pass
                return

    def _createBar(self, master):
        pass

    def addValue(self):
        if self._value <= self._allvalues:
            self._value += 1
            self._tempCount += 1

    def addSubValue(self):
        if self._value <= self._allvalues:
            self._value += 1
            self._tempCount += 1

    def getTime(self):
        if self._finishProgress:
            return t.time() - self._startTime
        else:
            return None

    def isBarFull(self):
        if self._value == self._allvalues:
            return False
        else:
            return True

if __name__ == '__main__':
    win = StartProgressBar(allvalues=10)
    while True:
        for i in range(10):
            win.addValue()
            t.sleep(1)
if __name__ == '__main_':
    win = StartProgressWindow("Please Wait")
    t.sleep(5)
    win.stop()
