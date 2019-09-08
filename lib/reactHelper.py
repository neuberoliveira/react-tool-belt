import sys
import os
import json

packageFile = 'package.json';
appFile 	= 'app.json';

def isProject():
	isReacNative = False;

	if os.path.isdir('./ios') and os.path.isdir('./android') :
		isReacNative = True;

	if not isReacNative :
		print 'Are you sure you are in a React Native project?';
		sys.exit();
