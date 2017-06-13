import sys
import subprocess
import argparse
from os import path

sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import command

args = command.createCommand('reverse');


host = args.protocol+':'+args.port;
subprocess.call(["adb", "reverse", host, host]);
print 'done'
