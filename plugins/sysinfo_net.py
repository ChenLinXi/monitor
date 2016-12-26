#coding:utf-8
import sys
sys.path.append('../')

from iPlugin import Plugin

__all__ = ["NetInfo"]

class NetInfo(Plugin):
	name = "NetInfo"
	version = '0.0.1'

	def __init__(self):
		self.ret = {'name':None,'out':None,'in':None}
		f = open('/proc/net/dev')
		self.lines = f.readlines()
		f.close()
		self.lines = self.lines[2:]
		Plugin.__init__(self)

	def extract(self):
		for line in self.lines:
			if line.lstrip():
				line = line.replace(':',' ')
				items = line.split()
				try:
					self.ret['name'] = str(items[0])
					self.ret['in'] = long(items[1])
					self.ret['out'] = long(items[len(items)/2+1])
				except ValueError:
					pass
			yield self.ret
