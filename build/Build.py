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
        self.addOption('inc', 'yes', 'automaticaly increment the build number by 1', str)
        self.addOption('version', None, 'set the version name', str)
        self.addOption('apk', None, 'path to move apk after build it (android ONLY)', str)

    def execute(self, args):
        self.platform = args.os
        reactHelper.isProject()
        needInc = self.str2bool(args.inc)
        androidBuilder = BuildAndroid(needInc, args.version, args.apk)

        if self.isBoth():
            androidBuilder.build();

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
