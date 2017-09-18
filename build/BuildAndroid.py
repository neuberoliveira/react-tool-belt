import os
import re
import glob
import shutil
import errno
import subprocess
from BuildInterface import BuildInterface

class BuildAndroid(BuildInterface):
    def __init__(self, inc, version, apkout):
        super(BuildAndroid, self).__init__(inc, version, "/android/app/build.gradle")
        self.output = apkout
        
    def extractInfo(self):
        versionMatch = re.search('versionName "(\d+(\.\d+(\.\d+)?)?)"', self.configContent)
        buildMatch = re.search('versionCode (\d+)', self.configContent)

        if versionMatch:
            self.versionName = versionMatch.group(1)

        if buildMatch:
            self.buildVersion = int(buildMatch.group(1))
    
    def setBuildName(self, version):
        versionMatch = re.search('versionName "(\d+(\.\d+(\.\d+)?)?)"', self.configContent)
        if versionMatch:
            fullMatch = versionMatch.group(0);
            self.configContent = self.configContent.replace(fullMatch, 'versionName "'+version+'"')
            print self.configContent
    
    def setBuildVersion(self, build):
        buildMatch = re.search('versionCode (\d+)', self.configContent)
        if buildMatch:
            fullMatch = buildMatch.group(0);
            self.configContent = self.configContent.replace(fullMatch, 'versionCode '+str(build))

    def runBuildScript(self):
        try:

            code = 0
            #code = subprocess.call(["./gradlew", "assembleRelease"], cwd="android")
            apkfile = './android/app/build/outputs/apk/app-release.apk'
            glogdirs = glob.glob('./node_modules/react-native/third-party/glog-*/')

            for glog in glogdirs:
                shutil.rmtree(glog)


            if code == 0:
                filename = ''
                dirname = ''
                if re.search('\.apk', self.output):
                    filename = os.path.basename(self.output)
                    dirname = os.path.dirname(self.output)
                else:
                    dirname = self.output
                    filename = 'release_v'+self.versionName+'-b'+str(self.buildVersion)+'.apk'

                dirname = dirname+'/'
                newApkPath = dirname+filename
                if os.path.exists(dirname):
                    subprocess.call(['cp', apkfile, newApkPath])
                    print 'APK moved to '+newApkPath

                else:
                    print 'The output dir for APK "'+dirname+'" doesnot exists'

        except subprocess.CalledProcessError as spex:
            print spex.returncode
            print spex.output
            print spex.message
        except OSError as ioex:
            print ioex.errno
            print ioex.strerror
