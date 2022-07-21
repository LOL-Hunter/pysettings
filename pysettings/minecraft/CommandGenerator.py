from pysettings.minecraft.mcConstants import *
from pyperclip import copy
from pysettings.geometry import Location3D





class _BossBar:
    def __init__(self, name):
        self.getAllBossBars = self.listBossBars
        self.name = name
        pass
    def createNewBossBar(self, title:str):
        return "/bossbar add "+str(self.name)+" \""+str(title)+"\""
    def getPlayers(self):
        return "/bossbar get minecraft:"+self.name+" players"
    def getValue(self):
        "/bossbar get minecraft:" + self.name + " value"
    def getVisible(self):
        "/bossbar get minecraft:" + self.name + " visible"
    def getMaxValue(self):
        "/bossbar get minecraft:" + self.name + " max"
    def setColor(self, c:BossBarColor):
        return "/bossbar set minecraft:"+self.name+" color "+c.value
    def setMaxValue(self, v:int):
        return "/bossbar set minecraft:"+self.name+" max "+str(v)
    def setTitle(self, t:str):
        return "/bossbar set minecraft:" + self.name + " title \"" + str(t)+"\""
    def setPlayers(self, _type:EntityType):
        return "/bossbar set minecraft:" + self.name + " players "+_type.value
    def setStyle(self, style:BossBarStyle):
        return "/bossbar set minecraft:" + self.name + " style " + style.value
    def setValue(self, v:int):
        return "/bossbar set minecraft:" + self.name + " value " + str(v)
    def setVisible(self, b:bool):
        return "/bossbar set minecraft:" + self.name + " visible " + str(bool(b)).lower()
    def listBossBars(self):
        return "/bossbar list"
    def removeBossBar(self):
        return "/bossbar remove minecraft:"+self.name


class CommandGenerator:
    @staticmethod
    def advancement():
        pass
    @staticmethod
    def attribute():
        pass
    @staticmethod
    def bossBar(name):
        return _BossBar(name)
    @staticmethod
    def clear(_type:EntityType, mat:Material=None, count=None):
        _type = _type.value
        if mat is not None: mat = mat.value
        if count is not None: count = str(count)
        return "/clear "+" ".join([i if i is not None else "" for i in (_type, mat, count)])
    @staticmethod
    def clone(from_:Location3D, to_:Location3D, target:Location3D):
        #TODO:Finish
        return f"/clone {from_.getX()} {from_.getY()} {from_.getZ()} {to_.getX()} {to_.getY()} {to_.getZ()} {target.getX()} {target.getY()} {target.getZ()}"
    @staticmethod
    def data():
        pass
    @staticmethod
    def dataPack():
        pass
    @staticmethod
    def debug():
        pass
    @staticmethod
    def defaultGameMode(gm:GameMode):
        return "/defaulgamemode "+gm.value
    @staticmethod
    def difficulty(mode:Difficulty):
        return "/difficulty "+mode.value
    @staticmethod
    def effectGive(target:EntityType, _type:Effect, duration, lvl):
        if hasattr(duration, "value") and duration.value == "maxValue": duration = 999999
        if hasattr(lvl, "value") and lvl.value == "maxValue": lvl = 255
        return "/effect give "+target.value+" "+_type.value+" "+str(duration)+" "+str(lvl)
    @staticmethod
    def effectClear(target:EntityType,_type:Effect=None):
        if _type is not None: _type = _type.value
        return "".join([i if i is not None else "" for i in ("/effect clear "+target.value+" ", _type)])
    @staticmethod
    def enchant(target:EntityType,_type:Enchantment, lvl:int):
        return "/enchant "+target.value+" "+_type.value+" "+str(lvl)
    @staticmethod
    def execute():
        pass
    @staticmethod
    def xp():
        pass
    @staticmethod
    def fill():
        pass
    @staticmethod
    def forceLoad():
        pass
    @staticmethod
    def function():
        pass
    @staticmethod
    def gameMode(gm:GameMode):
        return "/gamemode "+gm.value
    @staticmethod
    def gameRule(gameRule:GameRule, b):
        return "/gamerule "+gameRule.value+" "+str(bool(b)).lower()
    @staticmethod
    def give():
        pass
    @staticmethod
    def help():
        pass
    @staticmethod
    def kick():
        pass
    @staticmethod
    def kill():
        pass
    @staticmethod
    def list():
        pass
    @staticmethod
    def locate():
        pass
    @staticmethod
    def locateBiome():
        pass
    @staticmethod
    def loot():
        pass
    @staticmethod
    def me():
        pass
    @staticmethod
    def msg():
        pass
    @staticmethod
    def particle():
        pass
    @staticmethod
    def playSound():
        pass
    @staticmethod
    def publish():
        pass
    @staticmethod
    def recipe():
        pass
    @staticmethod
    def reload():
        pass
    @staticmethod
    def replaceItem():
        pass
    @staticmethod
    def say():
        pass
    @staticmethod
    def schedule():
        pass
    @staticmethod
    def scoreboard():
        pass
    @staticmethod
    def seed():
        pass
    @staticmethod
    def setBlock():
        pass
    @staticmethod
    def setWorldSpawn():
        pass
    @staticmethod
    def spawnPoint():
        pass
    @staticmethod
    def spectate():
        pass
    @staticmethod
    def spreadPlayers():
        pass
    @staticmethod
    def stopSound():
        pass
    @staticmethod
    def summon():
        pass
    @staticmethod
    def tag():
        pass
    @staticmethod
    def team():
        pass
    @staticmethod
    def teamMsg():
        pass
    @staticmethod
    def teleport():
        pass
    @staticmethod
    def tellRaw():
        pass
    @staticmethod
    def time():
        pass
    @staticmethod
    def title():
        pass
    @staticmethod
    def tp():
        pass
    @staticmethod
    def trigger():
        pass
    @staticmethod
    def weather():
        pass
    @staticmethod
    def worldBoarder():
        pass



if __name__ == '__main__':
    print(CommandGenerator.clone(Location3D(1, 1, 1), Location3D(2, 3, 4), Location3D(0, 0, 0)))