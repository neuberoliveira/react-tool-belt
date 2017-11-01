import os
import re
import sys
import glob
import shutil
import errno
import subprocess
import datetime
import getpass
import tempfile
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
        self.pbxprojHandler = open(os.getcwd() + '/ios/' + app_name + '.xcodeproj/project.pbxproj', 'r')
        

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
            FNULL = open(os.devnull, 'w')
            wsPodName = self.appName+'.xcworkspace'
            scriptdir = os.path.dirname(os.path.realpath(__file__))
            
            #archive
            print 'Archive project'
            
            #verify if a xcworkspace, normaly created from pods, exists and use is as workspace to archive
            archiveCmd = ["xcodebuild", "-scheme", self.appName];
            if os.path.isdir('./ios/'+wsPodName) :
                archiveCmd.append('-workspace')
                archiveCmd.append(wsPodName)
            
            archiveCmd.append('archive')
            archivecode = subprocess.call(archiveCmd, cwd="ios", stdout=FNULL)
            #archivecode = 0
            
            #format dates
            date = datetime.datetime.now()
            separator = "-"
            date_year = str(date.year)
            date_month = str(date.month).rjust(2, '0')
            date_day = str(date.day).rjust(2, '0')
            
            todaydir = date_year+separator+date_month+separator+date_day
            todayfileYearFull = date_day+separator+date_month+separator+date_year
            todayfileYear = date_day+separator+date_month+separator+date_year[2:]

            archivepath = os.getenv("HOME")+"/Library/Developer/Xcode/Archives/"+todaydir+"/"
            #archivepath = os.getenv("HOME")+"/Library/Developer/Xcode/Archives/2017-10-31/"
            
            archives = glob.glob(archivepath+self.appName+" "+todayfileYear+"*") + glob.glob(archivepath+self.appName+" "+todayfileYearFull+"*")
            #archives = glob.glob(archivepath+self.appName+"*")
            
            if archivecode==0 and len(archives)>0:
                print 'Archive OK'
                archivefile = archives[-1]
                #ipaname = self.appName+'_v'+self.versionName+'-b'+str(self.buildVersion)+'.ipa'
                
                #generate exportOptions
                print 'Generating Export Options...'
                provisioningInfo = self.getProvisioningName()
                tmpDir = tempfile.gettempdir()
                tmpfileName = self.appName+'_exportoptions.plist'
                tmpPath = tmpDir+'/'+tmpfileName
                
                exportTemplateHandler = open(scriptdir+"/ExportOptions_template.plist", 'r')
                exportHandler = open(tmpPath, 'w+')
                
                exportTemplate = exportTemplateHandler.read();
                
                exportTemplate = exportTemplate.replace('%BUNDLE_ID%', self.getBundleId())
                exportTemplate = exportTemplate.replace('%PROVISIONING_PROFILE%', provisioningInfo[0])
                
                exportHandler.write(exportTemplate)
                exportHandler.close()
                
                #export IPA
                print 'Generating IPA...'
                exportcode = subprocess.call(["xcodebuild", "-exportArchive", 
                    "-archivePath", archivefile,
                    "-exportPath", self.ipaout,
                    "-allowProvisioningUpdates",
                    "-exportOptionsPlist", tmpPath,
                ], cwd="ios", stdout=FNULL)
                
                if exportcode==0:
                    #print 'IPA moved to '+self.ipaout
                    print 'IPA OK'
            
            
            exportTemplateHandler.close()
            self.pbxprojHandler.close()
        except subprocess.CalledProcessError as spex:
            print spex.returncode
            print spex.output
            print spex.message
        except OSError as ioex:
            print ioex.errno
            print ioex.strerror

    def getProvisioningName(self):
        prov_name = None
        prov_uuid = None
                
        foundProvisioning = False
        foundRelease = False
        for line in self.pbxprojHandler.readlines():
            matches = re.findall('PROVISIONING_PROFILE(_SPECIFIER)?\s=\s"(.*)";', line)
            matcheRelease = re.search('name = Release;', line)
            if matches :
                foundProvisioning = True
                
                key = matches[0][0]
                value = matches[0][1]
                if key == '_SPECIFIER':
                    prov_name = value
                else :
                    prov_uuid = value
                
                
            if foundProvisioning and matcheRelease :
                foundRelease = True
                break
        
        if foundProvisioning and foundRelease :
            return (prov_uuid, prov_name)
        else:
            return None
    
    def getBundleId(self):
        self.pbxprojHandler.seek(0);
        match = re.search('PRODUCT_BUNDLE_IDENTIFIER = (.*);', self.pbxprojHandler.read())
        if match:
            return match.group(1)
        
        
        
        
