import re
from BuildInterface import BuildInterface

class BuildAndroid(BuildInterface):
    def __init__(self, inc, version):
        super(BuildAndroid, self).__init__(inc, version, "/android/app/build.gradle")
        
    def extractInfo(self):
        versionMatch = re.search('versionName "(\d+(\.\d+(\.\d+)?)?)"', self.configContent)
        buildMatch = re.search('versionCode (\d+)', self.configContent)

        if versionMatch:
            self.versionName = versionMatch.group(1)

        if buildMatch:
            self.buildVersion = int(buildMatch.group(1))
    
    def setBuildName(self, version):
        pass
    
    def setBuildVersion(self, build):
        pass