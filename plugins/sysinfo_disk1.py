#coding:utf-8

import os,sys,json,copy,time,math,struct,glob,re
import psutil
from collections import namedtuple
sys.path.append('../')
from iPlugin import Plugin

__all__ = ["DiskInfo"]

class DiskInfo(Plugin):
	name = "DiskInfo"
	version = '0.0.1'
	def __init__(self):
		self.ret = {'total':0,'free':0,'used':0,'read':0,'write':0}
		Plugin.__init__(self)

	def extract(self):
		diskInfo = psutil.disk_usage('/')
		diskRW = psutil.disk_io_counters()
		self.ret['total'] = diskInfo.total
		self.ret['free'] = diskInfo.free
		self.ret['used'] = diskInfo.used
		self.ret['read'] = diskRW.read_bytes
		self.ret['write'] = diskRW.write_bytes
		return self.ret
