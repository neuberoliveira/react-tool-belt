import os

class BuildInterface(object):
    def __init__(self, inc, version, configPath):
        self.version = version
        self.incBuild = inc
        
        self.configFile = os.getcwd()+'/'+configPath
        self.configHandler = open(self.configFile, 'r+')
        self.configContent = self.configHandler.read()

        self.versionName = None
        self.buildVersion = None

    def extractInfo(self):
        raise NotImplementedError("extractInfo method must be implemented")    

    def build(self):
        self.extractInfo()

        if self.incBuild:
            self.buildVersion = self.buildVersion + 1
            self.setBuildVersion(self.buildVersion)
        
        if self.version:
            self.setBuildName(self.version)