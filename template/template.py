import sys
import os

from lib import reactHelper

def toCamelCase(name) :
	camelCased = name;

	if '-' in name or '_' in name :
		camelCased = camelCased.replace('-', ' ');
		camelCased = camelCased.replace('_', ' ');
		camelCased = camelCased.title();
	
	camelCased = camelCased.replace(' ', '');
	
	return camelCased;

def execute(args) :
	#reactHelper.isProject();
	scriptDir = os.path.dirname(os.path.abspath(__file__));
	path = args.path;
	filename = args.name;
	classname = toCamelCase(args.name);
	
	if path==None :
		path = os.getcwd();
	
	template = open(scriptDir+'/templates/component.txt', 'r').read();
	newContent = template.replace('#CLASS_NAME#', classname);
	
	dstPath = path+'/'+classname+'.js';
	output = open(dstPath, 'w');
	output.write(newContent);
	output.close();
	
	print 'done';

