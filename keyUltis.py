import keyboard as k
import mouse as m
from pysettings.geometry import Location2D
from pysettings import Queue
from time import sleep


class Event:
    def __init__(self, dic=None):
        if dic is None:
            self.data = {"type":"",
                         "loc":None,
                         "key":None,
                         "args":[],
                         "func":None,
                         "value":None,
                         "disableArgs":False}
        else:
            self.data = dic.data
    def __getitem__(self, item):
        return self.data[item]
    def __setitem__(self, key, value):
        self.data[key] = value
    def __repr__(self):
        return f"Event(key:{self['key']} state:{self['state']})"
    def isKeyDown(self):
        return self["state"] == "down"
    def isKeyUp(self):
        return self["state"] == "up"
    def getKey(self):
        return self["key"]
    def getState(self):
        return self["state"]

class KeyListenerError:
    class InvalidListenerType(Exception):
        pass
    class MultipleListeners(Exception):
        pass

class EventHandler:
    KEY_EVENTS = []
    MOUSE_EVENTS = []
    def __init__(self, func, args, _type):
        self.func = func
        self.args = args
        self.type = _type
    def __call__(self, event):
        event["args"] = self.args
        out = self.func(event)

    @staticmethod
    def onKeyEvent(func=None, args=None):
        EventHandler.KEY_EVENTS.append(EventHandler(func, args, "all"))
        return func

    @staticmethod
    def onKeyPressEvent(func=None, args=None):
        EventHandler.KEY_EVENTS.append(EventHandler(func, args, "press"))
        return func

    @staticmethod
    def onKeyReleaseEvent(func=None, args=None):
        EventHandler.KEY_EVENTS.append(EventHandler(func, args, "release"))
        return func


    @staticmethod
    def onMouseMotionEvent(func=None, args=None):
        EventHandler.KEY_EVENTS.append(EventHandler(func, args, "motion"))
        return func

    @staticmethod
    def onMouseScrollEvent(func=None, args=None):
        EventHandler.KEY_EVENTS.append(EventHandler(func, args, "scroll"))
        return func

    @staticmethod
    def onMouseEvent(func=None, args=None):
        EventHandler.MOUSE_EVENTS.append(EventHandler(func, args, "all"))
        return func

    @staticmethod
    def onMousePressEvent(func=None, args=None):
        EventHandler.MOUSE_EVENTS.append(EventHandler(func, args, "press"))
        return func

    @staticmethod
    def onMouseReleaseEvent(func=None, args=None):
        EventHandler.MOUSE_EVENTS.append(EventHandler(func, args, "release"))
        return func


class _KeyBoardListener:
    def __init__(self, handler):
        self.handler:Listener = handler
        self.mousePos = Location2D(0, 0)
        k.hook(self._press)
        m.hook(self._click)

    def _click(self, args):
        """
        Motion: {'x': 1739, 'y': 58, 'time': 1644349210.576856}
        Click:  {'event_type': 'down', 'button': 'left', 'time': 1644349212.264588}
        Wheel:  {'delta': -1.0, 'time': 1644349213.2384164}

        @param args:
        @return:
        """
        if type(args) == m.ButtonEvent:
            _data = args._asdict()
            data = {"type":"mousePress",
                    "loc":Location2D(self.mousePos),
                    "state":_data["event_type"],
                    "button":_data["button"],
                    "time":_data["time"]}
            self.handler._triggerMousePress(data)
        elif type(args) == m.MoveEvent:
            _data = args._asdict()
            data = {"type":"mouseMotion",
                    "loc":Location2D(_data["x"], _data["y"]),
                    "time":_data["time"]}
            self.mousePos = data["loc"].clone()
            self.handler._triggerMouseMotion(data)
        elif type(args) == m.WheelEvent:
            _data = args._asdict()
            data = {"type":"mouseWheel",
                    "loc":Location2D(self.mousePos),
                    "time":_data["time"],
                    "delta":_data["delta"]}
            self.handler._triggerMouseScroll(data)

    def _press(self, args):
        """
        press:  {"event_type": "up", "scan_code": 17, "name": "w", "time": 1644348576.015082, "is_keypad": false}

        @param args:
        @return:
        """

        _data = args
        data = {"type":"Keyboard",
                "state":_data.event_type,
                "key":_data.name,
                "keyCode":_data.scan_code,
                "time":_data.time}
        self.handler._triggerKeyPress(data)


class Listener:
    _LISTENER = None
    def __init__(self):
        self.listener = _KeyBoardListener(self)
        Listener._LISTENER = self
        self.data = {
                "queue":Queue(),
                "mouseDown":[],
                "keyDown":[]
        }
    def __getitem__(self, item):
        return self.data[item]
    def __setitem__(self, key, value):
        self.data[key] = value
    def setEventHandler(self, e):
        """
        Use this function to pass your own handler class instance.
        Otherwise, the decorator wont work.

        @param e:
        @return:
        """
    def _triggerMouseScroll(self, data):
        event = Event()
        event.data = {**event.data, **data}
        self["queue"].append(event)

        for _event in EventHandler.MOUSE_EVENTS:
            if _event.type == "scroll":
                _event(event)
    def _triggerMousePress(self, data):
        event = Event()
        event.data = {**event.data, **data}
        self["queue"].append(event)

        for _event in EventHandler.MOUSE_EVENTS:
            if _event.type == "all":
                _event(event)
            elif _event.type == "press" and data["state"] == "down":
                if data["button"] in self.data["mouseDown"]:
                    _event(event)
            elif _event.type == "release" and data["state"] == "up":
                if data["button"] not in self.data["mouseDown"]:
                    _event(event)
        if data["state"] == "up":
            if data["button"] in self.data["mouseDown"]:
                self.data["mouseDown"].remove(data["button"])
        elif data["state"] == "down":
            if data["button"] not in self.data["mouseDown"]:
                self.data["mouseDown"].append(data["button"])
    def _triggerMouseMotion(self, data):
        event = Event()
        event.data = {**event.data, **data}
        self["queue"].append(event)

        for _event in EventHandler.MOUSE_EVENTS:
            if _event.type == "motion":
                _event(event)
    def _triggerKeyPress(self, data):
        event = Event()
        event.data = {**event.data, **data}
        self["queue"].append(event)

        for _event in EventHandler.KEY_EVENTS:
            if _event.type == "all":
                _event(event)
            elif _event.type == "press" and data["state"] == "down":
                #if data["key"] in self.data["keyDown"]: # add as Setting in decorator (*hold_key* trigger multiple times or just one)
                    _event(event)
            elif _event.type == "release" and data["state"] == "up":
                #if data["key"] not in self.data["keyDown"]:
                    _event(event)


        if data["state"] == "up":
            if data["key"] in self.data["keyDown"]:
                self.data["keyDown"].remove(data["key"])
        elif data["state"] == "down":
            if data["key"] not in self.data["keyDown"]:
                self.data["keyDown"].append(data["key"])
    def waitForKeyPress(self, key):
        while True:
            sleep(.1)
            if self.isKeyPressed(key):
                return True
    def waitForKeyRelease(self, key):
        while True:
            sleep(.1)
            if self.isKeyReleased(key):
                return True
    def isKeyPressed(self, key):
        if key in self["keyDown"]:
            return True
        return False
    def isKeyReleased(self, key):
        if key not in self["keyDown"]:
            return True
        return False
    def isMousePressed(self, key):
        if key in self["mouseDown"]:
            return True
        return False
    def isMouseReleased(self, key):
        if key not in self["mouseDown"]:
            return True
        return False
    def get(self):
        return self["queue"].get()
    def clearQueue(self):
        self["queue"].clear()
    def wait(self):
        try:
            while True:
                sleep(.1)
        except KeyboardInterrupt: return


if __name__ == '__main__':
    lis = Listener()
    @EventHandler.onKeyReleaseEvent
    def key(e):
        e = Event(e)
        print(e.getKey())
    lis.wait()