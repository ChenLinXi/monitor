#coding:utf-8
import sys,psutil
sys.path.append('../')

from iPlugin import Plugin

__all__ = ["CpuInfo"]

class CpuInfo(Plugin):
	name = "CpuInfo"
	version = '0.0.1'

	def __init__(self):
		self.ret = {'cpuNum':None,'usr':None,'sys':None,'idl':None,'wai':None,'hiq':None,'siq':None}
		Plugin.__init__(self)
	def extract(self):
		res = psutil.cpu_times_percent(interval=2,percpu=False)
		f = open('/proc/stat')
		lines = f.readlines()
		f.close()
		count = -1
		for l in lines:
			l = l.split()
			if l[0][0:3] == 'cpu':
				count += 1
		self.ret['cpuNum'] = count
		self.ret['usr'] = res.user
		self.ret['sys'] = res.system
		self.ret['idl'] = res.idle
		self.ret['wai'] = res.iowait
		self.ret['hiq'] = res.irq
		self.ret['siq'] = res.softirq

		return self.ret		
