import sys
import os

from lib import reactHelper
from lib import ModuleInterface

class Template(ModuleInterface):
    def __init__(self):
        super(Template, self).__init__()
        self.name = 'template'
        self.prog = 'Template'
        self.help = 'Generate an class file with all the imports stuffs'

        self.addOption('name', None, 'Name of the class', str, False)
        self.addOption('path', None, 'Path to save the file, defaults to current directory')

    def _toCamelCase(self, name):
        camelCased = name

        if '-' in name or '_' in name:
            camelCased = camelCased.replace('-', ' ')
            camelCased = camelCased.replace('_', ' ')
            camelCased = camelCased.title()
        
        camelCased = camelCased.replace(' ', '')
        
        return camelCased

    def execute(self, args):
        reactHelper.isProject()
        scriptDir = os.path.dirname(os.path.abspath(__file__))
        path = args.path
        filename = args.name
        classname = self._toCamelCase(args.name)
        
        if path==None:
            path = os.getcwd()
        
        template = open(scriptDir+'/templates/component.txt', 'r').read()
        newContent = template.replace('#CLASS_NAME#', classname)
        
        dstPath = path+'/'+classname+'.js'
        output = open(dstPath, 'w')
        output.write(newContent)
        output.close()
        
        print 'done'

