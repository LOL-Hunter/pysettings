import pysettings as pys


class CommandParser:
    def __init__(self, parameters, withCommand=False):
        self.command = []
        self.argsList = {}
        self.commandName = None
        self.usage = None

        if type(parameters) == str:
            self.command = parameters.split(" ")
        elif type(parameters) == list:
            self.command = parameters
        else:
            pass
        if withCommand:
            self.commandName = self.command[0]
            self.command.pop(0)
        for i in range(len(self.command)):
            if self.command[i].startswith("-"):
                name = self.command[i][1:]
                if len(self.command)-1 < i+1 or self.command[i + 1].startswith("-"):
                    value = ""
                else:
                    value = self.command[i + 1]
                self.argsList[name.replace("-", "")] = value
    def __getitem__(self, item):
        if list(self.argsList.keys()).__contains__(item):
            return self.argsList[item]
        return None
    def getArg(self, *e, _type=str):
        try:
            return _type([self[str(i)] for i in e if self.argsList.__contains__(i)][0])
        except:
            return None
    def length(self):
        return len(self.command)
    def getParameterList(self):
        return self.command
    def contaisParameter(self, *param):
        return any([list(self.argsList.keys()).__contains__(i) for i in param])

class FileSizeParser:
    @staticmethod
    def parseToString(size):
        units = ["b", "K", "M", "T", "P"]
        for i in units:
            if size < 1024:
                return f"{size:.2f}{i}"
            size /= 1024




if __name__ == '__main_':
    parser = CommandParser(input("-->"), withCommand=True, argsSeperator=" ")
    print("length:", parser.length())
    print("parameters:", parser.getParameterList())
    print("args:", parser.getArgsList())
if __name__ == '__main__':
    parser = CommandParser(input("-->"),withCommand= True)
    print(parser.argsList)
