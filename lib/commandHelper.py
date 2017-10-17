import subprocess

class Option(object):
    def __init__(self, name, shortname, default, help, type=str):
        self.name = name
        self.shortname = shortname
        self.default = default
        self.type	= type
        self.help = help

    def getName(self, shortname=False):
        return self.name
    
    def getShortName(self):
        return self.shortname
    
    def isPositional(self):
        return True if self.shortname==None else False


class CommandList(object):
    list = []
    
    def add(self, cmd):
        self.list.append(cmd)
    
    def find(self, name):
        cmdFound = None
        for cmd in self.list:
            if cmd.name==name :
                cmdFound = cmd
                break
        
        return cmdFound
