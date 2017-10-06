import sys
import subprocess
import argparse
import os
import json

from lib import ModuleInterface
from lib import reactHelper
from BuildAndroid import BuildAndroid 
from BuildIOS import BuildIOS 

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
        self.addOption('inc', 'yes', 'automaticaly increment the build number by 1', str)
        self.addOption('version', None, 'set the version name', str)
        self.addOption('output', None, 'path to move binary to', str)

    def execute(self, args):
        self.platform = args.os
        reactHelper.isProject()
        packageJson = json.load(open('./package.json'));
        needInc = self.str2bool(args.inc)
        androidBuilder = BuildAndroid(packageJson['name'], needInc, args.version, args.output)
        iosBuilder = BuildIOS(packageJson['name'], needInc, args.version, args.output)

        if self.isBoth():
            iosBuilder.build();
            androidBuilder.build();
        elif self.isDroid():
            androidBuilder.build();
        elif self.isIOS():
            iosBuilder.build();
        else:
            print "Unavailable platform '"+self.platform+"' choose one of both, android, ios"
        
        print 'done'

    def isDroid(self):
        return self.platform == PLATFORM_ANDROID

    def isIOS(self):
        return self.platform == PLATFORM_IOS

    def isBoth(self):
        return self.platform == PLATFORM_BOTH
    
    def str2bool(self, v):
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')
