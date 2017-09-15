import sys
import subprocess
import argparse
import os

from lib import ModuleInterface
from lib import reactHelper
from BuildAndroid import BuildAndroid 

PLATFORM_BOTH = 'both'
PLATFORM_ANDROID = 'android'
PLATFORM_IOS = 'ios'

class Build(ModuleInterface):
    def __init__(self):
        super(Build, self).__init__()
        self.name = 'build'
        self.prog = 'Build'
        self.help = 'Build the app for release'

        self.addOption('os', PLATFORM_BOTH, 'build only the platform especific (android,ios)', str)
        self.addOption('inc', True, 'automaticaly increment the build number by 1', bool)
        self.addOption('version', None, 'set the version name', str)

    def execute(self, args):
        self.platform = args.os
        #reactHelper.isProject()
        androidBuilder = BuildAndroid(args.inc, args.version)

        if self.isBoth():
            androidBuilder.build();

        print 'done'

    def isDroid(self):
        return self.platform == PLATFORM_ANDROID

    def isIOS(self):
        return self.platform == PLATFORM_IOS

    def isBoth(self):
        return self.platform == PLATFORM_BOTH
    
    def buildDroid(self, inc, version):
        if inc:
            self.incBuild()

        os.chdir("android")
        subprocess.call(["./gradlew", "assembleRelease"])
        print('done');
