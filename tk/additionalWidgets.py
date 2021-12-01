from pysettings import tk

class DataVirtualizer(tk.Widget):
    def __init__(self, _master, autoRender=True):
        if isinstance(_master, dict):
            self.data = _master
        elif isinstance(_master, tk.Tk) or isinstance(_master, tk.Frame) or isinstance(_master, tk.LabelFrame):
            self.data = {"master": _master, "widget": tk._tk_.LabelFrame(_master._get())}
            self._canvas = tk.Canvas(master)
            self._scX = tk.Scale(master, orient=tk.Scale.HORIZONTAL, from_=1, to=1000).setValue(100).setBg(tk.Color.rgb(150, 150, 150)).onScroll(self._update)
            self._scY = tk.Scale(master, orient=tk.Scale.VERTICAL, from_=1, to=1000).setValue(100).setBg(tk.Color.rgb(150, 150, 150)).onScroll(self._update)
            self._isPoints = tk.Checkbutton(master, text="ShowPoints").setSelected().setBg(tk.Color.rgb(150, 150, 150)).onSelectEvent(self._update, args=["render"])
            self._autoRender = tk.Checkbutton(master, text="AutoRender").setValue(autoRender).setBg(tk.Color.rgb(150, 150, 150)).onSelectEvent(self._update)
            self._renderBtn = tk.Button(master, text="Render").setCommand(self._update, args=["render",])
            self.__isPoints = True
            self._maxValuesX = 100
            self._maxValuesY = 100
            self._dotWidth = 4
            self._drawedValues = 0
            self._lastPoint = tk.Location2D(0, 0)
            self._values = [0]
        else:
            raise tk.TKExceptions.InvalidWidgetTypeException("_master must be " + str(self.__class__.__name__) + ", Frame or Tk instance not: " + str(_master.__class__.__name__))
        super().__init__(self, self.data)
    def reset(self):
        self._lastPoint = tk.Location2D(0, self._canvas.getHeight()-10)
        self._canvas.clear()
        self._drawedValues = 0
        self._values = [0]
        return self
    def _update(self, e):
        if self._autoRender.getValue() or (e == "render" or (hasattr(e, "getArgs") and e.getArgs() is not None and e.getArgs()[0] == "render")):
            self._maxValuesX = self._scX.getValue()
            self._maxValuesY = self._scY.getValue()
            self.__isPoints = self._isPoints.getValue()
            _values = self._values.copy()
            self.reset()
            for value in _values[1:]:
                self.addValues(value)
    def addValues(self, args):
        assert self["alive"], "Widget must be placed before drawing values!"
        self._drawedValues += 1
        if ((self._canvas.getWidth()-10)/self._maxValuesX)*self._drawedValues < self._canvas.getWidth():
            pointLoc = tk.Location2D((((self._canvas.getWidth()-10)/self._maxValuesX)*self._drawedValues), self._canvas.getHeight()-tk._map(args, 0, self._maxValuesY, 10, self._canvas.getHeight()-10))
            if self.__isPoints:
                circ = tk.CanvasCircle(self._canvas).setLocation(pointLoc.clone().change(x=-int(self._dotWidth/2), y=-int(self._dotWidth/2))).setWidth(self._dotWidth).setHeight(self._dotWidth).setBg("black")
                circ.render()
            line = tk.CanvasLine(self._canvas).setLocation(self._lastPoint).setSecondLoc(pointLoc)
            line.render()
            self._lastPoint = pointLoc
            if args > max(self._values):
                #resize
                pass
        self._values.append(args)
    def place(self, x=0, y=0, width=200, height=200, anchor:tk.Anchor=tk.Anchor.UP_LEFT):
        assert not self["destroyed"], "The widget has been destroyed and can no longer be placed."
        if hasattr(anchor, "value"):
            anchor = anchor.value
        self.placeForget()
        if isinstance(x, tk.Location2D):
            x, y = x.get()
        x = int(round(x, 0))
        y = int(round(y, 0))
        self._canvas.place(0, 0, width-width*.1, height-height*.1)
        self._lastPoint = tk.Location2D(0, self._canvas.getHeight()-10)
        self._scX.place(0, height-height*.1,  width-width*.1, height*.1)
        self._scY.place(width-width*.1, 0, width*.1, height-height*.1)
        self._isPoints.place(width-width*.1, height-height*.1, width*.1)
        self._autoRender.place(width - width * .1, height - height * .1 + 25, width*.1)
        self._renderBtn.place(width - width * .1, height - height * .1 + 50, width*.1)
        self["widget"].place(x=x, y=y, width=width, height=height, anchor=anchor)
        self["alive"] = True
        return self




if __name__ == '__main__':
    from random import randint
    from time import sleep


    master = tk.Tk()
    master.setWindowSize(1000, 800)
    sc = tk.ScrollBar(master)

    sc.place(0, 0, 100)

    vit = DataVirtualizer(master)
    #vit.place(0, 0, 1000, 800)
    #for i in range(0, 1000):
       #vit.addValues(randint(0, 1000))


    master.mainloop()