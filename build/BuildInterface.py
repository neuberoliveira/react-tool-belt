import os
import re

class BuildInterface(object):
    def __init__(self, app_name, inc, version, configPath):
        self.version = version
        self.incBuild = inc
        self.appName = app_name
        
        self.configFile = os.getcwd()+'/'+configPath
        
        self.versionName = None
        self.buildVersion = None

        configHandler = open(self.configFile, 'r')
        self.configContent = configHandler.read()
        configHandler.close()

    def runBuildScript(self):
        raise NotImplementedError("runBuildScript method must be implemented")

    def extractInfo(self):
        raise NotImplementedError("extractInfo method must be implemented")

    def setBuildVersion(self):
        raise NotImplementedError("setBuildVersion method must be implemented")

    def setBuildName(self, version):
        raise NotImplementedError("setBuildName method must be implemented")
    
    def beforeSaveConfig(self):
        pass

    def build(self):
        self.extractInfo()
        if self.incBuild or self.version:
            if self.incBuild:
                self.buildVersion = self.buildVersion+1;
                self.setBuildVersion()
            
            if self.version:
                self.versionName = self.version
                self.setBuildName(self.version)
            
            self.beforeSaveConfig()
            configHandler = open(self.configFile, 'w+')
            configHandler.write(self.configContent)
            configHandler.close()
        
        self.runBuildScript();