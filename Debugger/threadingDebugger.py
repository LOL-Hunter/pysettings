import threading as th
from random import randint
import time as t

class Settings:
    MESSURE_TIME = False
    DEBUG_PRINT = True
    ID = True

class Thread:
    THREAD_NUMBER = 0
    def __init__(self, target, args=()):
        self.id = "".join([str(randint(0, 9)) for _ in range(8)])
        self.target = target
        self._thread = th.Thread(target=self._run)
    def start(self):
        self._thread.start()
    def _run(self):
        f = t.time()
        Thread.THREAD_NUMBER += 1
        if Settings.DEBUG_PRINT: print("[THREAD-"+str(Thread.THREAD_NUMBER)+"-STARTED]: Function: "+self.target.__name__+" | id:"+self.id)
        self.target()
        Thread.THREAD_NUMBER -= 1
        if Settings.DEBUG_PRINT: print("[THREAD-" + str(Thread.THREAD_NUMBER) + "-STOPPED]: Function: " + self.target.__name__ + " | id:" + self.id, "" if not Settings.MESSURE_TIME else "Time: "+str(round(t.time()-f, 5)))
