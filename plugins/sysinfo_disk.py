#coding:utf-8

import os,sys,json,copy,time,math,struct,glob,re
from collections import namedtuple
sys.path.append('../')
from iPlugin import Plugin

__all__ = ["DiskInfo"]

class DiskInfo(Plugin):
	name = "DiskInfo"
	version = '0.0.1'
	def __init__(self):
		self.disk_ntuple = namedtuple('partition', 'device mountpoint fstype')
		self.usage_ntuple = namedtuple('usage','total used free percent')
		Plugin.__init__(self)

	def disk_partitions(self,all=False):
		phydevs = []
		f = open('/proc/filesystems')
		for line in f:
			if not line.startswith("nodev"):
				phydevs.append(line.strip())
		retlist = []
		f = open('/etc/mtab')
		for line in f:
			if not all and line.startswith('none'):
				continue
			fields = line.split()
			device = fields[0]
			mountpoint = fields[1]
			fstype = fields[2]
			if not all and fstype not in phydevs:
				continue
			if device == 'none':
				device = ''
			ntuple = self.disk_ntuple(device, mountpoint, fstype)
			retlist.append(ntuple)
		return retlist

	def disk_usage(self,path):
		st = os.statvfs(path)
		free = long(st.f_bavail* st.f_frsize*1024)
		total = long(st.f_blocks * st.f_frsize*1024)
		used = long((st.f_blocks - st.f_bfree) * st.f_frsize*1024)
		try:
			percent = ret = (float(used)/total) * 100
		except ZeroDivisionError:
			percent = 0
		return self.usage_ntuple(total, used, free, round(percent, 1))




		
