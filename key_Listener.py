import sys
import keyboard as k
import keyboard.mouse as m

class LSettings:
    def __init__(self):
        self._settings = {"keyUp":False, "keyDown":False}

    def OnlyKeyUp(self, boolean):
        if type(boolean) is bool:
            self._settings["keyUp"] = boolean
            return self
        else:
            raise TypeError("Wrong settingType: "+str(type(boolean))+" use Bool!")
    def OnlyKeyDown(self, boolean):
        if type(boolean) is bool:
            self._settings["keyDown"] = boolean
            return self
        else:
            raise TypeError("Wrong settingType: " + str(type(boolean)) + " use Bool!")

    def _get(self):
        return self._settings
class _Mouse:
    def __init__(self, ins):
        self._ins = ins
        self.ClickEvent = _ClickEvent(self._ins)
        self.Wheel = _Wheel(self._ins)
        self.MoveEvent = _MoveEvent(self._ins)

        self.LEFT = "left"
        self.MIDDLE = "middle"
        self.RIGHT = "right"
        self.FORWARD = "x2"
        self.BACKWARD = "x"
        self.MOUSEUP = "up"
        self.MOUSEDOWN = "down"
        self.SCROLLFORWARD = 1
        self.SCROLLBACKWARD = -1
class _Wheel:
    def __init__(self, ins):
        self._ins = ins

    def getState(self, wait=False):
        while True:
            if self._ins._mouseScrollDelta != None:
                temp = self._ins._mouseScrollDelta
                self._ins._mouseScrollDelta = None
                return int(temp)
            else:
                if not wait:
                    return None

    def getLastMouseScrollTime(self):
        if self._ins._lastMouseScrollTime != None:
            temp = self._ins._lastMouseScrollTime
            self._ins._lastMouseScrollTime = None
            return temp
class _MoveEvent:
    def __init__(self, ins):
        self._ins = ins

    def getMouseMovement(self, wait=False):
        while True:
            if self._ins._mouseX != None:
                x = self._ins._mouseX
                self._ins._mouseX = None
                y = self._ins._mouseY
                self._ins._mouseY = None
                return (x, y)
            else:
                if not wait:
                    return (None, None)

    def getLastMouseClickTime(self):
        if self._ins._lastMouseMoveTime != None:
            temp = self._ins._lastMouseMoveTime
            self._ins._lastMouseMoveTime = None
            return temp
class _ClickEvent:
    def __init__(self, ins):
        self._ins = ins

    def isDoubleClick(self, interval = 0.500, wait=False):
        while True:
             if self._ins._timeDiffToLastClick != None and self._ins._timeDiffToLastClick < interval:
                self._ins._timeDiffToLastClick = None
                return True
             else:
                 if not wait:
                    return False

    def getState(self, wait=False, btn=None):
        while True:
            if self._ins._mouseEventType != None:
                temp = self._ins._mouseEventType
                self._ins._mouseEventType = None
                if self._ins._button == btn:
                    return temp
                elif btn == None:
                    return temp
            elif not wait:
                return None

    def isAnyButtonClicked(self, state="down", wait=False):
        while True:
            if self._ins._button != None:
                temp = self._ins._button
                self._ins._button = None
                if state != None:
                    if state == self.getState():
                        return True
                else:
                    return False
            else:
                if not wait:
                    return False

    def getClickedButton(self, wait=False, state="down"):
        while True:
            if self._ins._button != None:
                temp = self._ins._button
                self._ins._button = None
                if state != None:
                    if state == self.getState():
                        return temp

                else:
                    return temp
            else:
                if not wait:
                    return None

    def getLastMouseClickTime(self):
        if self._ins._lastMouseClickTime != None:
            temp = self._ins._lastMouseClickTime
            self._ins._lastMouseClickTime = None
            return temp
class _Letters:
    def __init__(self):
        self.a = "a"
        self.A = "A"
        self.b = "b"
        self.B = "B"
        self.c = "c"
        self.C = "C"
        self.d = "d"
        self.D = "D"
        self.e = "e"
        self.E = "E"
        self.f = "f"
        self.F = "F"
        self.g = "g"
        self.G = "G"
        self.h = "h"
        self.H = "H"
        self.i = "i"
        self.I = "I"
        self.j = "j"
        self.J = "J"
        self.k = "k"
        self.K = "K"
        self.l = "l"
        self.L = "L"
        self.m = "m"
        self.M = "M"
        self.n = "n"
        self.N = "N"
        self.o = "o"
        self.O = "O"
        self.p = "p"
        self.P = "P"
        self.q = "q"
        self.Q = "Q"
        self.r = "r"
        self.R = "R"
        self.s = "s"
        self.S = "S"
        self.t = "t"
        self.T = "T"
        self.u = "u"
        self.U = "U"
        self.v = "v"
        self.V = "V"
        self.w = "w"
        self.W = "W"
        self.x = "x"
        self.X = "X"
        self.y = "y"
        self.Y = "Y"
        self.z = "z"
        self.Z = "Z"
class _SpecialLetters:
    def __init__(self):
        pass
class _keys:
    def __init__(self):
        self.RETURN = "enter"
        self.BACKSPACE = "backspace"
        self.ALT = "alt"
        self.LWIN = "linke windows"
        self.ALTGR = "alt gr"
        self.TAB = "tab"
        self.SPACE = "space"
        self.SHIFT = "umschalt"
        self.RSHIFT = "right shift"

        self.Letters = _Letters()
        self.SpecialLetters = _SpecialLetters()
class _Keyboard:
    def __init__(self, ins):
        self._keycache = None
        self._ins = ins
        self.KEYUP = "up"
        self.KEYDOWN = "down"

    def isKeyPressed(self, key, waitFor=False, state="down"):
        while True:
            if self._ins._name == key:
                if state != None:
                    if self.getState() == state:
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                if not waitFor:
                    return False

    def getKey(self, state="down", wait = False):
        while True:
            l = self._ins._name
            if l != None:
                self._ins._name = None
                if state != None:
                    if self.getState() == state:
                        return l
                else:
                    return l
            else:
                if not wait:
                    return l

    def getKeyCode(self):
        if self._ins._keyCode != None:
            temp = self._ins._keyCode
            self._ins._keyCode = None
            return temp

    def getState(self, wait=False):
        while True:
            if self._ins._state != None:
                temp = self._ins._state
                self._ins._state = None
                return temp
            else:
                if not wait:
                    return None

    def getLastKeyPressedTime(self):
        if self._ins._lastButtonPressedTime != None:
            temp = self._ins._lastButtonPressedTime
            self._ins._lastButtonPressedTime = None
            return temp
class Listener:
    def __init__(self, Settings = None):
        if Settings is None:
            self._settings = LSettings()._get()
        else:
            self._settings = Settings._get()
            print(self._settings)
        self._keyUP = self._settings["keyUp"]
        self._keyDown = self._settings["keyDown"]

        self._doubbleFireList = []
        self._old = 1000000000000

        #keyboard:
        self._name = None
        self._keyCode = None
        self._state = None
        self._lastButtonPressedTime = None
        #Mouse:
            #move:
        self._mouseX = None
        self._mouseY = None
        self._lastMouseMoveTime = None
            #Click:
        self._timeDiffToLastClick = None
        self._mouseEventType = None
        self._button = None
        self._lastMouseClickTime = None
            #Wheel:
        self._mouseScrollDelta = None
        self._lastMouseScrollTime = None

        k.hook(self._press)
        m.hook(self._click)

        self.Mouse = _Mouse(self)
        self.KeyBoard = _Keyboard(self)
        self.Keys = _keys()
    def _click(self, args):
        if str(args).startswith("MoveEvent"):
            self._mouseX = args.x
            self._mouseY = args.y
            self._lastMouseMoveTime = args.time
        elif str(args).startswith("ButtonEvent"):
            self._mouseEventType = args.event_type
            self._button = args.button
            self._lastMouseClickTime = args.time
            if args.event_type == "down": self._calcClickDiff(args)
        elif str(args).startswith("WheelEvent"):
            self._mouseScrollDelta = args.delta
            self._lastMouseScrollTime = args.time
    def _press(self, args):
        self._manageKeyDoubbleFire(args.name)
        self._name = args.name
        self._keyCode = args.scan_code
        self._lastButtonPressedTime = args.time
    def _calcClickDiff(self, args):
        self._timeDiffToLastClick = args.time - self._old
        self._old = args.time
    def _manageKeyDoubbleFire(self, key):
        if self._doubbleFireList.__contains__(key):
            self._doubbleFireList.remove(key)
            self._state = "up"
        else:
            self._state = "down"
            self._doubbleFireList.append(key)

if __name__ == '__main__':
    l = Listener()
    while True:
        if l.KeyBoard.isKeyPressed(l.Keys.TAB, False, l.KeyBoard.KEYDOWN):
            print("Tab pressed")



