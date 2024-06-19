import time as t
import random as rd
from pysettings.text import MsgText

def timerBenchmark(func, times=10):
    timings = []
    for i in range(times):
        startTime = t.time()
        MsgText.info(f"Starting benchmark [{i}/{times}]...")
        c = 0
        while True:
            func()
            c += 1
            if t.time()-startTime > 1:
                timings.append(c)
                break
        MsgText.info(f"Starting benchmark [{i}/{times}] ended! Times run in one sec {c}")
    MsgText.info(f"\n=== Benchmark End ===")
    timings.sort()
    MsgText.info(f"Average run Time: {sum(timings) / len(timings)}")

def iterDict(__iterable:dict):
    return zip(__iterable.keys(), __iterable.values())
class IndependentTimer:
    """
    This modified time.time() can hold the time during a time change by the system.
    Because timeit.timeit() is too slow :)

    ==example==
    if not IndependentTimer.getChangingTimeInProgress():            #checks if another time change is still in progress
        IndependentTimer.save()                                     #saves time for all timers
        os.system(<change sys time>)                                #change system time
        IndependentTimer.release()                                  #releases the saved time for all timers
    """
    _changingTime = False
    _Timers = []
    def __init__(self):
        IndependentTimer._Timers.append(self)
        self._time = t.time()
        self._saveTime = 0
    def __str__(self):
        return str(t.time()-self._time)
    @staticmethod
    def getTimerPaused():
        return IndependentTimer._changingTime
    def match(self, time):
        return t.time()-self._time >= time
    def reset(self):
        self._time = t.time()
    def destroy(self):
        IndependentTimer._Timers.remove(self)
    @staticmethod
    def save():
        IndependentTimer._changingTime = True
        for timer in IndependentTimer._Timers:
            timer._saveTime = t.time() - timer._time
    @staticmethod
    def release():
        for timer in IndependentTimer._Timers:
            timer._time = t.time()+timer._saveTime
        IndependentTimer._changingTime = False
class ID:
    @staticmethod
    def newId(length:int):
        return "".join([str(rd.randint(0, 9)) for _ in range(length)])
class Queue:
    def __init__(self):
        self.isGettingInProg = False
        self.queue = []
        self._queue = []

    def append(self, i):
        if self.isGettingInProg:
            self._queue.append(i)
        else:
            self.queue.append(i)

    def get(self):
        self.isGettingInProg = True
        temp = self.queue.copy()
        self.queue = []
        self.isGettingInProg = False

        self.queue.extend(self._queue)
        self._queue = []

        return temp

    def __len__(self):
        return len(self.queue)

    def clear(self):
        self.queue = []
        self._queue = []
class DataClass:
    def __init__(self):
        self.data = {}
    def __getitem__(self, item):
        if list(self.data.keys()).__contains__(item):
            return self.data[item]
        else:
            raise KeyError("key \""+str(item)+"\" is not in Dict!")
    def __setitem__(self, key, value):
        self.data[key] = value