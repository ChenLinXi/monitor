#coding:utf-8
import sys,psutil,glob,os,re,time
sys.path.append('../')
from iPlugin import Plugin

__all__ = ["UtilsInfo"]

class UtilsInfo(Plugin):
	name = "UtilsInfo"
	version = '0.0.1'
	
	def __init__(self):
		self.ret = psutil.disk_io_counters(perdisk=False)
		self.time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
		self.ports = []

		self.f = glob.glob('/proc/*')
		self.count = 0
		for i in self.f:
			if re.search("([a-z/]*)([0-9]*)",i):
				self.count += 1

		Plugin.__init__(self)

	def diskRW(self): #get disk_write and disk_read
		return self.ret

	def processCount(self):
		return self.count

	def getSysTime(self):
		return self.time

	def getPorts(self):
		stream = os.popen('netstat -anptl')
		lines = stream.readlines()
		result = []
		for line in lines:
			line=line.lstrip()
			line=line.split()
			res = line[3].split(":")
			if len(res) == 2:
				result.append(res[1])
		for i in result:
			self.ports.append(int(i))
		self.ports = list(set(self.ports))
		return self.ports
