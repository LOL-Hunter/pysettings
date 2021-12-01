import os, json
class _JsonConfig:
    def __init__(self, data, path):
        self.data = data
        self.path = path
        self.save = self.saveConfig
    def __setitem__(self, key, value):
        self.data[key] = value
    def __getitem__(self, item):
        if list(self.data.keys()).__contains__(item):
            return self.data[item]
        else:
            return None
    def __repr__(self):
        return str(self.data)
    def keys(self):
        return list(self.data.keys())
    def values(self):
        return list(self.data.values())
    def clearData(self):
        self.data = {}
        return self
    def getData(self):
        return self.data
    def setData(self, d):
        if isinstance(d, dict):
            self.data = d.copy()
        else:
            self.data = d.data
        return self
    def saveConfig(self, beauty=True):
        file = open(self.path, "w")
        if beauty:
            file.write(json.dumps(self.data, indent=4))
        else:
            file.write(json.dumps(self.data))
        file.close()
class JsonConfig:
    @staticmethod
    def isConfigAvailable(path):
        return os.path.exists(path)
    @staticmethod
    def loadConfig(path, create=False):
        if not os.path.exists(path):
            if create:
                file = open(path, "w")
                file.write("{}")
                file.close()
            else: raise FileExistsError("Config file does not exists.: "+path)
        file = open(path, "r")
        text=""
        for line in file:
            text+=line
        file.close()

        try:
            data = json.loads(text.replace("\n", "").replace("'", "\"").replace("(", "[").replace(")", "]"))
        except json.JSONDecodeError as e:
            line = e.lineno
            col = e.colno
            pos = e.pos
            textLine = text.split("\n")[line-1]

            if len(textLine)-pos > 10:
                to_ = pos+10
            else:
                to_ = pos - len(textLine)

            if pos >= 10:
                from_ = pos-10
            else:
                from_ = 0
            err = "\nThis ConfigFile is corrupted or not readable!\n\nFile: "+path+"\nLine:"+str(line-1)+"\nchar:"+str(pos)+"\nException type: "+str(e.msg)+"\n\nInvalid Syntax Here:\n"+("..." if from_ > 0 else "")+textLine[from_:to_]+"...\n"+" "*((pos+2) if from_ > 0 else pos-1)+"^"
            raise Exception(err)
        return _JsonConfig(data, path)



if __name__ == '__main__':
    JsonConfig.loadConfig(r"C:\Users\langh\Desktop\test.txt")