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
    def getPrettifyData(self):
        return json.dumps(self.data, indent=4)
    def setData(self, d):
        if isinstance(d, dict) or isinstance(d, list):
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
    def loadConfig(path, create=False, ignoreErrors=False):
        if not os.path.exists(path):
            if create:
                file = open(path, "w")
                file.write("{}")
                file.close()
            else: raise FileExistsError("Config file does not exists.: "+path)
        file = open(path, "rb")
        text = file.read()
        file.close()
        data = JsonConfig._decode(path, text, ignoreErrors)
        if isinstance(data, list) or isinstance(data, dict):
            return _JsonConfig(data, path)
        return data
    @staticmethod
    def fromString(s:str, ignoreErrors=False):
        data = JsonConfig._decode("", s.encode(), ignoreErrors)
        return data
    @staticmethod
    def prettifyString(s:str, ignoreErrors=False):
        data = JsonConfig.fromString(s, True)
        if isinstance(data, dict) or isinstance(data, list):
            return str(json.dumps(data, indent=4))
        if ignoreErrors:
            return data
        raise Exception(data)

    @staticmethod
    def _decode(path, s:bytes, ignoreErrors):
        try:
            data = json.loads(s.replace(b"\n", b"").replace(b"(", b"[").replace(b")", b"]"))  # .replace(b"'", b"\""))
        except json.JSONDecodeError as e:
            line = e.lineno
            col = e.colno
            pos = e.pos
            textLine = s.split(b"\n")[line - 1]
            if len(textLine) - pos > 10:
                to_ = pos + 10
                dots = True
            else:
                to_ = len(textLine)
                dots = False
            if pos >= 10:
                _dots = True
                from_ = pos - 10
            else:
                _dots = False
                from_ = 0
            err = "\nThis ConfigFile is corrupted or not readable!\n\nFile: " + path + "\nLine: " + str(
                line - 1) + "\nchar: " + str(pos) + "\nException type: " + str(e.msg) + "\n\nInvalid Syntax Here:\n" + (
                      "..." if _dots > 0 else "") + textLine[from_:to_].decode() + ("...\n" if dots else "\n")
            err += " " * ((pos - from_) if not _dots else (pos - from_ + 3)) + "^"
            if not ignoreErrors:
                raise Exception(err)
            return err
        return data



if __name__ == '__main__':
    JsonConfig.loadConfig(r"C:\Users\langh\Desktop\test.txt")