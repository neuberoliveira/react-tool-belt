#!/usr/bin/python
import sys
import os
import argparse
import subprocess
import json
from CommandHelper import Command,Option,CommandList

list = CommandList();

cmdReverse = Command('reverse', 'Reverse', 'Call adb reverse PROTOCOL:PORT PROTOCOL:PORT');
cmdReverse.addOption('port', '8081', 'port to reverse');
cmdReverse.addOption('protocol', 'tcp', 'protocol to reverse');
list.add(cmdReverse);

cmdResource = Command('resource', 'Resource', 'Generate app icon for ios and android. Image must be 1024px');
cmdResource.addOption('icon', None, 'Path to icon file');
list.add(cmdResource);

def createCommand(name):
	cmd = list.find(name);
	if not cmd :
		print 'Ops! Command not found';
		sys.exit();
	
	parser = argparse.ArgumentParser(prog=cmd.name, description=cmd.help);

	for opt in cmd.options :
		parser.add_argument(opt.getName(), action='store', type=opt.type, default=opt.default, help=opt.help);
	
	args = parser.parse_args();
	return args;
		
	

def checkReactProject():
	isReacNative = False;
	packageFile = 'package.json';
	
	if os.path.exists(packageFile) :
		checks = 0;
		package = json.load(open(packageFile));
		dependencies = package['dependencies'];
		
		for pack in dependencies :
			if pack=='react' or pack=='react-native' :
				checks += 1;
		
		if checks>=2 :
			isReacNative = True;
	
	if not isReacNative :
		print 'Are you sure you are in a React Native project?';
		sys.exit();
	
