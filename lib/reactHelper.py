import sys
import os
import json

packageFile = 'package.json';
appFile 	= 'app.json';

def isProject():
	isReacNative = False;

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
