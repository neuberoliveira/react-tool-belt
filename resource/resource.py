import sys
import os
import subprocess
import argparse
import imghdr
import json
from PIL import Image

from lib import commandCreator
from lib import reactHelper
import sizemap


def generateAndroid(image):
	platform = sizemap.icon['android'];
	ext = platform['format'];

	for item in platform['sizes'] :
		size = item['size'];
		dir = item['dir'];
		name = item['name'];

		drawableDir = platform['basedir']+dir
		destinationPath = drawableDir+name+'.'+ext;

		if not os.path.exists(drawableDir) :
			os.makedirs(drawableDir);

		tmpImage = image.resize((size, size), resample=Image.LANCZOS);
		tmpImage.save(destinationPath, format=ext, quality=100);


def generateIOS(image):
	package = json.load(open('package.json'));
	projectName = package['name'];

	platform 	= sizemap.icon['ios'];
	ext 		= platform['format'];
	basedir 	= platform['basedir'].replace('{{projectname}}', projectName);

	jsonStruct 		= {};

	jsonStruct['images'] 	= [];
	jsonStruct['info'] 	= {'version':1, 'author':'xcode'};

	for item in platform['sizes'] :
		size 	= item['size'];
		name 	= item['name'];
		idiom 	= item['idiom'];
		scale 	= item['scale'];
		realsize = int(size * scale);

		filename = name+'.'+ext;
		destinationPath = basedir+filename;

		sizeStr = str(size)+'x'+str(size);
		scaleStr = str(scale)+'x';
		jsonStruct['images'].append({
			'idiom': idiom,
			'size': sizeStr,
			'filename': filename,
			'scale': scaleStr,
		});


		if not os.path.exists(basedir) :
			os.makedirs(basedir);

		tmpImage = image.resize((realsize, realsize), resample=Image.LANCZOS);
		tmpImage.save(destinationPath, format=ext, compress_level=9);

	formated = json.dumps(jsonStruct, sort_keys=False, indent=2, separators=(',', ': '));
	jsonHandler = open(basedir+'Contents.json', 'w+');
	jsonHandler.write(formated);
	jsonHandler.close();


def execute(args) :
	filename = args.icon;
	availableFormats = ['png'];
	reactHelper.isProject();

	if not filename :
		print 'No file specified.'
		sys.exit()

	if not os.path.isfile(filename) :
		print 'The file "'+filename+'" not exists or is not valid file';
		sys.exit()

	format = imghdr.what(filename);
	image = None;

	try:
		availableFormats.index(format);
		image = Image.open(filename);
	except Exception as e:
		print 'The image is not in valid format, formats available are: '+str(availableFormats);
		sys.exit()

	print "Generate Android icons";
	generateAndroid(image);

	print "Generate IOS icons";
	generateIOS(image);

	print 'done';
