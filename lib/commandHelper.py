import subprocess

class Command:
	name = None;
	prog = None;
	help = None;
	options = [];
	
	def __init__(self, name, prog, help):
		self.name = name;
		self.prog = prog;
		self.help = help;
		self.options = [];
	
	def addOption(self, name, default, help, type=str, optional=True):
		self.options.append(Option(name, default, help, type, optional));
		
	
class Option:
	name = None;
	default = None;
	type = str;
	help = None;
	optional = True;
	
	def __init__(self, name, default, help, type=str, optional=True):
		self.name = name;
		self.default = default;
		self.type	= type;
		self.help = help;
		self.optional	= optional;

	def getName(self, shortname=False):
		if self.optional :
			return  self._getShortName() if shortname else self._getFullName();
		else:
			return self.name;
	
	def _getFullName(self):
		return '--'+self.name;
	
	def _getShortName(self):
		return '-'+self.name.substr(0, 1);
	
	
class CommandList:
	list = [];
	
	def add(self, cmd):
		self.list.append(cmd);
	
	def find(self, name):
		cmdFound = None;
		for cmd in self.list:
			if cmd.name==name :
				cmdFound = cmd;
				break;
		
		return cmdFound;
