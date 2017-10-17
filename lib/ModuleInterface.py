from commandHelper import Option

class ModuleInterface(object):
    def __init__(self):
        self.name = None
        self.prog = None
        self.help = None
        self.options = []

    def addOption(self, name, shortname, default, help, type=str):
        self.options.append(Option(name, shortname, default, help, type))

    def getOptions(self):
        return self.options;

    def execute(self, args):
        raise NotImplementedError("execute method must be implemented");