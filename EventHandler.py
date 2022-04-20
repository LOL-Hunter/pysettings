from pysettings import DataClass
class Errors:
    class InvalidEventType(Exception):
        pass


class RawEvent:
    def __init__(self, dic):
        if dic is None:
            self.data = {}
        elif isinstance(dic, RawEvent):
            print(dic.data)
            self.data = dic.data
        else:
            raise Errors.InvalidEventType(type(dic) + "is not a valid EventType! [<type:dict> or <type:NoneType>]")
    def __getitem__(self, item):
        return self.data[item]
    def __setitem__(self, key, value):
        self.data[key] = value
    def _getEventBuilder(self):
        return EventBuilder(self)


class EventBuilder(DataClass):
    def __init__(self, event:RawEvent):
        super().__init__()
        self.data = event.data
    def addParameter(self, name, initialVal=None):
        self[name] = initialVal
    def getParameter(self, name):
        return self[name]


class CancelableEvent(RawEvent):
    def __init__(self, dic):
        super().__init__(dic)
        self["setCanceled"] = False
    def setCanceled(self, b:bool):
        self["setCanceled"] = b
    def getCanceled(self):
        return self["setCanceled"]


class EventRegistry(DataClass):
    def __init__(self):
        super().__init__()
        self.data = {"events":{}}
    def registerEvent(self, name, func):
        self["events"][name] = func

    def removeEvent(self, name):
        del self["events"][name]

    def triggerEvent(self, name, event:RawEvent):
        self.data["events"][name](event)
        return event
_REGISTRY = EventRegistry()



class EventHandler:
    @staticmethod
    def registerEvent(func):
        _REGISTRY.registerEvent(func.__name__, func)
        return func
    @staticmethod
    def triggerEvent(name, event:RawEvent):
        _REGISTRY.triggerEvent(name, event)













