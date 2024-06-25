# pysettings 
This python library is used in many of my projects. \
It provides several useful features listed and documented below.

## Installation
Note: This library is unfortunately not registered in pip yet.

* Download Repos
* Unzip folder
* rename it to "pysettings"
* move to python Lib folder 
* run ``pip install -r requirements.txt`` to install required packages.


## Documentation
### pysettings.tk
This sub package is a wrapper around tkinter. \
It provides several features to used tkinter a lot faster and easier. \
This sub package is usable as standalone version: \
For further documentation refer to the standalone version [simpletk](https://github.com/LOL-Hunter/tksimple).

### pysettings.geometry
##### Location2D
Creates a Location in 2-dimensional area.
```python
location = Location2D()
```
Access values through getter or method.
```python
x = location.getX()
x = location.x
```
Change values through setter or method.
```python
location.setX(10)
location.x = 10
location.change(x=10)
```
Compare two Locations.
```python
loc1 = Location2D(10, 15)
loc2 = Location2D(10, 15)

if loc1 == loc2:
    pass
```
##### Location3D
This class has the same features as Location2D in 3D.
##### Rect
This class is used to describe Rectangles in 2D. \
The main use is collision detection.

Create new Rect.
```python
rect = Rect(
    Location2D(0, 0),
    Location2D(10, 10)
)

rect = Rect.fromLocWidthHeight(Location2D(0, 0), 10, 10)
```
Get width and height.  
```python
width = rect.getWidth()
height = rect.getHight()
width = rect.width
height = rect.height
width, height = rect.getSize()
```
Clone Rect.
```python
rect2 = rect.clone()
```
Collision with Rect and Location. \
Returns true if Rect contains Location2D.  
```python
rect.collisionWithPoint(Location2D(2, 2))
```
Collision with Rect and Rect. \
Returns true if two Rects overlap.  
```python
rect.collisionWithRect(rect2)
```
Resizes the Rect but keeps a gives Ratio (rect2).  
```python
rect.resizeToRectWithRatio(rect2)
```
##### Circle
Create new Circle. 
```python
circ = Circle.fromCenterRadius(center=Location2D(10, 10), radius=10)
```
Collision with Circle and Location. \
Returns true if Circle contains Location2D.  
```python
circ.collisionWithPoint(Location2D(2, 2))
```
##### map_
Re-maps a number from one range to another.
```python
out = map_(value, inMin, inMax, outMin, outMax)
```

### pysettings.jsonConfing
Better JsonConfig than the default 'json' package.
#### JsonConfig
Create JsonConfig. \
Returns _JsonConfig instance explained below.
```python
conf = JsonCofig.loadConfig("data.json")
conf = JsonCofig.loadConfig("data.json", create=True) # creates empty config if it doesnt exist
conf = JsonConfig.fromDict({"test":1})
conf = JsonConfig.fromString("{\"test\":1}")
```
Some utility methods.  
```python
JsonConfig.isConfigAvailable("data.json") # checks if config is available
JsonConfig.prettifyString("{\"test\":1}") # returns data as string to print out.
JsonConfig.prettifyData({"test":1})
```
JsonConfig instance methods. \
get / set values.
```python
value = conf["test"]
conf["test"] = 2
conf.get("test", default=2) # if key does not exist
```
Default implemented dict methods.
```python
conf.keys()
conf.values()
```
overwrite data. / Clear Data.
```python
conf.setData({})
conf.clear()
```
overwrite path.
```python
conf.setPath("/config/data.json")
```
save config.
```python
conf.saveConfig(True) # (Default) json syntax is written in multiple lines.
conf.saveConfig(True) # json syntax is written in one line.
```
#### AdvancedJsonConfig
This feature is useful if multiple config files are used from one folder. \
if this config file gets deleted or corrupted it gets recreated with default data automatically.

Example.
```python

AdvancedJsonConfig.setConfigFolderPath("/config")
config = AdvancedJsonConfig(name="TestConfig")
config.setDefault({
    "test":1
})
config.load("data.json")
```

### pysettings.text
#### MsgText
Colored logging methods.
```python
MsgText.info("info")
MsgText.warning("warning")
MsgText.help("help")
MsgText.error("error")
```
<span style="color:green">[INFO-11:28:59]: info</span> \
<span style="color:yellow">[WARNING-11:28:59]: warning</span> \
<span style="color:yellow">[HELP]: help</span> \
<span style="color:red">[ERROR-11:28:59]: error</span>
