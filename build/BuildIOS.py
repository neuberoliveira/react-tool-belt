import os
import re
import sys
import glob
import shutil
import errno
import subprocess
import datetime
import getpass
import xml.etree.ElementTree as ET
from BuildInterface import BuildInterface

class BuildIOS(BuildInterface):
    def __init__(self, app_name, inc, version, ipaout):
        super(BuildIOS, self).__init__(app_name, inc, version, "/ios/"+app_name+"/Info.plist")
        self.xml = ET.fromstring(self.configContent)
        self.propsList = self.xml.find('dict')
        self.ipaout = ipaout
        self.CFBundleVersion_index = -1
        self.CFBundleShortVersionString_index = -1


    def extractInfo(self):
        bundleVersion = 0
        versionName = ""
        i = 0
        for child in self.propsList:
            if child.tag=='key' and child.text=='CFBundleVersion':
                self.CFBundleVersion_index = i+1
                el = self.propsList[self.CFBundleVersion_index]
                bundleVersion = int(el.text)
            
            if child.tag=='key' and child.text=='CFBundleShortVersionString':
                self.CFBundleShortVersionString_index = i+1
                el = self.propsList[self.CFBundleShortVersionString_index]
                versionName = el.text
            
            i = i+1;
        
        self.versionName = versionName
        self.buildVersion = int(bundleVersion)
    
    def beforeSaveConfig(self):
        self.configContent = ET.tostring(self.xml)


    def setBuildName(self, version):
        el = self.propsList[self.CFBundleShortVersionString_index]
        el.text = version
    
    def setBuildVersion(self):
        el = self.propsList[self.CFBundleVersion_index]
        el.text = str(self.buildVersion)

    def runBuildScript(self):
        
        try:
            scriptdir = os.path.dirname(os.path.realpath(__file__))
            date = datetime.datetime.now()
            separator = "-"
            date_year = str(date.year)
            date_month = str(date.month).rjust(2, '0')
            date_day = str(date.day).rjust(2, '0')
            
            todaydir = date_year+separator+date_month+separator+date_day
            todayfile = date_day+separator+date_month+separator+date_year[2:]
            
            #archive
            print 'Archive project'
            archivecode = subprocess.call(["xcodebuild", "-scheme", self.appName, "archive"], cwd="ios")
            
            archivepath = os.getenv("HOME")+"/Library/Developer/Xcode/Archives/"+todaydir+"/"
            pattern = archivepath+self.appName+" "+todayfile+"*"
            archives = glob.glob(pattern)
            
            if archivecode==0 and len(archives)>0:
                archivefile = archives[-1]
                #ipaname = self.appName+'_v'+self.versionName+'-b'+str(self.buildVersion)+'.ipa'
                
                #export IPA
                print 'Generating IPA'
                exportcode = subprocess.call(["xcodebuild", "-exportArchive", 
                    "-archivePath", archivefile,
                    "-exportPath", self.ipaout,
                    "-exportOptionsPlist", scriptdir+"/exportOptions.plist"
                ], cwd="ios")
                
                if exportcode==0:
                    print 'IPA moved to '+self.ipaout

        except subprocess.CalledProcessError as spex:
            print spex.returncode
            print spex.output
            print spex.message
        except OSError as ioex:
            print ioex.errno
            print ioex.strerror
