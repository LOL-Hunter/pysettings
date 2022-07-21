import keyboard as k
import mouse as m
from pysettings.geometry import Location2D
from pysettings import Queue
from enum import Enum
from pyautogui import press


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

class _PyInputListener:
    def __init__(self, handler):
        pass

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

class ListenerType(Enum):
    PYNPUT = _PyInputListener
    KEYBOARD = _KeyBoardListener

class Listener:
    _LISTENER = None
    def __init__(self, _type:ListenerType=ListenerType.KEYBOARD):
        if Listener._LISTENER is not None:
            raise KeyListenerError.MultipleListeners("You cannot use multiple Listeners!")
        if _type == ListenerType.KEYBOARD:
            self.listener = _KeyBoardListener(self)
        elif _type == ListenerType.PYNPUT:
            self.listener = _PyInputListener(self)
        else:
            raise KeyListenerError.InvalidListenerType("There is not type named: "+str(_type)+"\n Use the 'ListenerType' enum to choose a Listener class!")
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
                if data["key"] not in self.data["keyDown"]:
                    _event(event)


        if data["state"] == "up":
            if data["key"] in self.data["keyDown"]:
                self.data["keyDown"].remove(data["key"])
        elif data["state"] == "down":
            if data["key"] not in self.data["keyDown"]:
                self.data["keyDown"].append(data["key"])

    def waitForKeyPress(self, key):
        while True:
            if self.isKeyPressed(key):
                return True

    def waitForKeyRelease(self, key):
        while True:
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
            while True: pass
        except KeyboardInterrupt: return



if __name__ == '__main__':
    lis = Listener()

    @EventHandler.onKeyEvent
    def key(e):
        if e.getKey() == "space":
            press("w")

    lis.wait()