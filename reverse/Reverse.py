import sys
import subprocess
import argparse
from os import path

from lib import ModuleInterface

class Reverse(ModuleInterface):
    def __init__(self):
        super(Reverse, self).__init__()
        self.name = 'reverse'
        self.prog = 'Reverse'
        self.help = 'Call adb reverse PROTOCOL:PORT PROTOCOL:PORT'
        
        self.addOption('--port', None, '8081', 'port to reverse')
        self.addOption('--protocol', None, 'tcp', 'protocol to reverse')

    def execute(self, args):
        host = args.protocol+':'+args.port
        subprocess.call(["adb", "reverse", host, host])
        print 'done'
