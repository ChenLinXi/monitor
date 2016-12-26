#coding:utf-8
import sys,os,psutil
sys.path.append('../')

from iPlugin import Plugin

__all__ = ["MemInfo"]

class MemInfo(Plugin):
	name = "MemInfo"
	version = '0.0.1'

	def __init__(self):
		self.ret = {'total':0,'free':0,'buffers':0,'cached':0}
		Plugin.__init__(self)

	def extract(self):
		mem = psutil.virtual_memory()
		self.ret['total'] = mem.total
		self.ret['free'] = mem.free
		self.ret['buffers'] = mem.buffers
		self.ret['cached'] = mem.cached
		return self.ret
