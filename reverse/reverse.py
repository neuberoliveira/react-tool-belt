import sys
import subprocess
import argparse
from os import path

def execute(args) :
	host = args.protocol+':'+args.port;
	subprocess.call(["adb", "reverse", host, host]);
	print 'done'

