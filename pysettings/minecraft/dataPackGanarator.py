from pysettings.jsonConfig import JsonConfig
from pysettings.minecraft.mcConstants import Material
from pysettings.tk import FileDialog, SimpleDialog
from pysettings.text import MsgText
from pysettings.geometry import Location2D, Location3D, _map, Rect
from enum import Enum
import os, sys, shutil

class _OnTick:
    def __init__(self, name):
        self.data = {"path": "minecraft\\tags\\functions",
                     "extention":".json",
                     "name": str(name),
                     "ingredients":{},
                     "mcFunctionData":{
                         "values":[]
                        }
                     }
    def _getData(self):
        return self["mcFunctionData"]

    def __getitem__(self, item):
        return self.data[item]
    def __setitem__(self, key, value):
        self.data["key"] = value
    def addFunction(self, c):
        self["mcFunctionData"]["values"].append("custom:"+str(c["name"]))
        return self
class _McFunction:
    def __init__(self, name):
        self.data = {"path": "custom\\functions",
                     "extention":".mcfunction",
                     "name": str(name),
                     "ingredients":{},
                     "mcFunctionData":{
                         "code":[]
                        }
                     }
    def _getData(self):
        return "\n".join(self["mcFunctionData"]["code"])

    def __getitem__(self, item):
        return self.data[item]
    def __setitem__(self, key, value):
        self.data["key"] = value
    def addLine(self, c):
        self["mcFunctionData"]["code"].append(str(c))
        return self
class _SmithingRecipe:
    def __init__(self, name):
        self.data = {"path": "custom\\recipes",
                     "extention": ".json",
                     "name": str(name),
                     "ingredients":{},
                     "craftingData":{
                         "type":"smithing",
                         "base":{},
                         "addition":{},
                         "result":{},
                        }
                     }
    def _getData(self):
        return self.data["craftingData"]
    def __getitem__(self, item):
        return self.data[item]
    def __setitem__(self, key, value):
        self.data["key"] = value
    def setBase(self, itm:Material):
        self["craftingData"]["base"] = {"item":itm.value}
        return self
    def setAddition(self, itm:Material):
        self["craftingData"]["addition"] = {"item":itm.value}
        return self
    def setResult(self, itm:Material):
        self["craftingData"]["result"] = {"item":itm.value}
        return self
class _StoneCuttingRecipe:
    def __init__(self, name):
        self.data = {"path": "custom\\recipes",
                     "extention": ".json",
                     "name": str(name),
                     "ingredients": [],
                     "craftingData": {
                         "type": "stonecutting",
                         "ingredient":{},
                         "result":"material:air",
                         "count":1
                        }
                     }
    def _getData(self):
        return self.data["craftingData"]
    def __getitem__(self, item):
        return self.data[item]
    def __setitem__(self, key, value):
        self.data["key"] = value
    def setIngredient(self, itm:Material):
        self["craftingData"]["ingredient"] = {"item":itm.value}
        return self
    def setResult(self, itm:Material, count:int=1):
        self["craftingData"]["result"] = itm.value
        self["craftingData"]["count"] = count
        return self
class _FurnaceRecipe:
    def __init__(self, name):
        self.data = {"path": "custom\\recipes",
                     "extention": ".json",
                     "name": str(name),
                     "ingredients":{},
                     "craftingData":{
                         "type":"smelting",
                         "ingredient": {},
                         "result": "minecraft:glass",
                         "experience": 0.1,
                         "cookingtime": 200,
                         "count":1
                        }
                     }
    def _getData(self):
        return self.data["craftingData"]
    def __getitem__(self, item):
        return self.data[item]
    def __setitem__(self, key, value):
        self.data["key"] = value
    def setIngredient(self, itm:Material):
        self["craftingData"]["ingredient"] = {"item":itm.value}
        return self
    def setResult(self, itm:Material, count:int=1):
        self["craftingData"]["result"] = itm.value
        self["craftingData"]["count"] = count
        return self
    def setCookTime(self, t:int):
        self["craftingData"]["cookingtime"] = t
        return self
    def setExperience(self, e:float):
        self["craftingData"]["experience"] = e
        return self
class _ShapedCraftingRecipe:
    def __init__(self, name):
        self.data = {"path": "custom\\recipes",
                     "extention": ".json",
                     "name": str(name),
                     "ingredients":[],
                     "craftingData":{
                         "type":"crafting_shaped",
                         "pattern":[],
                         "key":{},
                         "result": {
                             "item": "minecraft:air",
                             "count": 3
                         }
                        }
                     }
    def _getData(self):
        return self.data["craftingData"]
    def __getitem__(self, item):
        return self.data[item]
    def __setitem__(self, key, value):
        self.data["key"] = value
    def setShape(self, *args:str):
        if len(args) <= 3 and all([len(i)==3 for i in args]):
            self["craftingData"]["pattern"] = list(args)
        else:
            raise ValueError("Could not parse Recipe!")
        return self
    def setIngredients(self, **kwargs): #TODO TAGS zb "Planks"
        d = {}
        for i in kwargs.keys():
            d[i] = {"item":kwargs[i].value}
        self["craftingData"]["key"] = d
        return self
    def setResult(self, mat:Material, count=1):
        self["craftingData"]["result"]["item"] = mat.value
        self["craftingData"]["result"]["count"] = count
class _ShapelessCraftingRecipe:
    def __init__(self, name):
        self.data = {"path": "custom\\recipes",
                     "extention": ".json",
                     "name": str(name),
                     "ingredients":[],
                     "craftingData":{
                         "type":"crafting_shapeless",
                         "ingredients":[],
                         "result": {
                             "item": "minecraft:air",
                             "count": 1
                         }
                        }
                     }
    def _getData(self):
        return self.data["craftingData"]
    def __getitem__(self, item):
        return self.data[item]
    def __setitem__(self, key, value):
        self.data["key"] = value
    def setIngredients(self, *items:Material):
        self.data["craftingData"]["ingredients"] = [{"item":i.value} for i in items]
        return self
    def setResult(self, mat:Material, count=1):
        self["craftingData"]["result"]["item"] = mat.value
        self["craftingData"]["result"]["count"] = count
        return self
class Generator:
    def __init__(self, name):
        self.data = {"name":str(name),
                     "description":"1"
                     }
        self.tasks = []
        self.path = None
        self.onTick = _OnTick("tick")
        self._overWriteWarning = True
    def __getitem__(self, item):
        return self.data[item]
    def __setitem__(self, key, value):
        self.data[key] = value

    def newShapedCraftingRecipe(self, name):
        r = _ShapedCraftingRecipe(name)
        self.tasks.append(r)
        return r
    def newShapelessCraftingRecipe(self, name):
        r = _ShapelessCraftingRecipe(name)
        self.tasks.append(r)
        return r
    def newFurnaceRecipe(self, name):
        r = _FurnaceRecipe(name)
        self.tasks.append(r)
        return r
    def newSmokerRecipe(self, name):
        r = _FurnaceRecipe(name)
        r.data["craftingData"]["type"] = "smoking"
        self.tasks.append(r)
        return r
    def newBlastingRecipe(self, name):
        r = _FurnaceRecipe(name)
        r.data["craftingData"]["type"] = "blasting"
        self.tasks.append(r)
        return r
    def newCampFireRecipe(self, name):
        r = _FurnaceRecipe(name)
        r.data["craftingData"]["type"] = "campfire_cooking"
        self.tasks.append(r)
        return r
    def newStoneCuttingRecipe(self, name):
        r = _StoneCuttingRecipe(name)
        self.tasks.append(r)
        return r
    def newSmithingRecipe(self, name):
        r = _SmithingRecipe(name)
        self.tasks.append(r)
        return r
    def newFunction(self, name, onTick=False):
        r = _McFunction(name)
        if onTick: self.onTick.addFunction(r)
        self.tasks.append(r)
        return r

    def setDescription(self, desc):
        self["description"] = str(desc)
    def setPath(self, p):
        if os.path.exists(p):
            self.path = p
        else:
            MsgText.error("This path does not exists: "+str(p))
    def setOverwriteWarning(self, b):
        self._overWriteWarning = b
    def _deleteDataPack(self):
        shutil.rmtree(self.path+"\\"+self["name"], ignore_errors=True)
    def generate(self):
        if self.path is None:
            _path = FileDialog.openDirectory(initialpath=r"C:\Users\langh\AppData\Roaming\.minecraft\saves\1"[0:-1])
            if _path is not None:
                self.path = _path
            else:
                MsgText.error("This path does not exists: "+str(_path))
                return
        if os.path.exists(self.path+"\\"+self["name"]):
            if self._overWriteWarning:
                if SimpleDialog.askYesNo("Overwrite existing Datapack?"):
                    self._deleteDataPack()
                else:
                    return
            else:
                self._deleteDataPack()
        os.mkdir(self.path+"\\"+self["name"])
        data = {"pack": {"pack_format": 7,"description": "None"}}
        data["pack"]["description"] = self["description"]
        JsonConfig.loadConfig(self.path+"\\"+self["name"]+"\\"+"pack.mcmeta", create=True).setData(data).saveConfig(beauty=True)
        os.mkdir(self.path + "\\" + self["name"] + "\\" + "data")
        os.mkdir(self.path + "\\" + self["name"] + "\\data\\" + "minecraft")
        os.mkdir(self.path + "\\" + self["name"] + "\\data\\" + "custom")
        os.mkdir(self.path + "\\" + self["name"] + "\\data\\" + "custom\\functions")
        os.mkdir(self.path + "\\" + self["name"] + "\\data\\" + "minecraft\\tags")
        self.tasks.append(self.onTick)
        for i in self.tasks:
            if not os.path.exists(self.path+"\\" + self["name"] +"\\data\\"+i["path"]):
                os.mkdir(self.path+"\\" + self["name"] +"\\data\\"+i["path"])
            if isinstance(i._getData(), dict):
                JsonConfig.loadConfig(self.path+"\\" + self["name"] +"\\data\\"+i["path"]+"\\"+i["name"]+i["extention"], True).setData(i._getData()).saveConfig(True)
            else:
                file = open(self.path+"\\" + self["name"] +"\\data\\"+i["path"]+"\\"+i["name"]+i["extention"], "w")
                file.write(i._getData())
                file.close()


if __name__ == '__main__':
    g = Generator(name="GunDataPack")
    g.setPath(r"C:\Robert\Minecraft\Server\Server-modded\1.16.5 (GunMod)\world\datapacks")
    g.setDescription("This is a Description!")
    g.newFunction("start", onTick=False).addLine('/setblock 19 4 -44 minecraft:redstone_block')
    #g.newFunction("reset", onTick=False).addLine("/setblock 19 4 -52 minecraft:redstone_block")
    g.generate()