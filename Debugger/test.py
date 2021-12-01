from pysettings.EventHandler import CustomEventTypes, Event



class MyEventHandler(CustomEventTypes):

    @CustomEventTypes.registerEvent
    def onClick(self, e):
        pass