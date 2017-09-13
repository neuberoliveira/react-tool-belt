from commandHelper import Option

class ModuleInterface(object):
    def __init__(self):
        self.name = None
        self.prog = None
        self.help = None
        self.options = []

    def addOption(self, name, default, help, type=str, optional=True):
        self.options.append(Option(name, default, help, type, optional))

    def getOptions(self):
        return self.options;

    def execute(self, args):
        raise NotImplementedError("execute method must be implemented");