#coding:utf-8

from pluginManager import DirectoryPluginManager
import os,json,copy,time,math,struct,glob,re,psutil,commands
from socket import *

class UdpClient(object):
	UDPSock = socket(AF_INET,SOCK_DGRAM)
	def __init__(self, server='xxxx',port=41235,mtu=1024,source=None):
		self.server = server
		self.port = int(port)
		self.mtu = int(mtu)
		self.source = source if source else gethostname()

	def chunks(self, data):
		chunk_size = self.mtu - 12
		total_chunks = int(math.ceil(len(data) / float(chunk_size)))
		count = 0
		message_id = hash(str( time.time()) + self.source)
		for i in xrange(0, len(data), chunk_size):
			header = struct.pack("!ccqBB",'\x1e','\x0f',message_id,count,total_chunks)
			count += 1
			yield header + data[i:i+chunk_size] #single return gelf package(1024B) in order

	def send(self, send_data):
		message = {}
		message['version'] = '1.0'
		message['short_message'] = 'tcbase.systeminfo'
		message['host'] = self.source
		message['timestamp'] = time.time()
		message['full_message'] = json.dumps(send_data)

		message_str = json.dumps(message,sort_keys=True).encode('utf-8')
		for chunk in self.chunks(message_str):
			self.UDPSock.sendto(chunk, (self.server, self.port))

def prepare():
	plugin_manager = DirectoryPluginManager()
	plugin_manager.loadPlugins()

	plugin_list = ["CpuInfo","DiskInfo","UtilsInfo","NetInfo","MemInfo"]
	res = {'net_dev':None,'net_send':None,'net_recv':None,'disk_read':None,'disk_write':None}

	net_list = []
	NetPlugin = plugin_manager.getPlugins(plugin_list[3])
	for part in NetPlugin[0].extract():
		if part['name'] == 'bond0':
			net_list.append(copy.copy(part)) #deep copy
			break
		else:
			pass
	time.sleep(8)
	return net_list

def getCpuLoad():
	(status, result) = commands.getstatusoutput('uptime')
	if status == 0 :
		return float(result.strip(' ').split(',')[4])
	else:
		return 0

def perform(net_list):
	plugin_manager = DirectoryPluginManager()
	plugin_manager.loadPlugins()

	net_info = net_list
	plugin_list = ["CpuInfo","DiskInfo","UtilsInfo","NetInfo","MemInfo"]
	res = {'net_dev':None,'net_send':None,'net_recv':None,'disk_read':None,'disk_write':None}


	CpuPlugin = plugin_manager.getPlugins(plugin_list[0])
	cpu_ret = CpuPlugin[0].extract()

	res['cpuNum'] = cpu_ret['cpuNum']
	res['usr'] = cpu_ret['usr']
	res['sys'] = cpu_ret['sys']
	res['idl'] = cpu_ret['idl']
	res['wai'] = cpu_ret['wai']
	res['hiq'] = cpu_ret['hiq']
	res['siq'] = cpu_ret['siq']
	res['load'] = getCpuLoad()

	DiskPlugin = plugin_manager.getPlugins(plugin_list[1])
	disk_ret = DiskPlugin[0].extract()
	res['diskFree'] = long(disk_ret['free'] * 1024)
	res['diskUsed'] = long(disk_ret['used'] * 1024)
	res['diskTotal'] = long(disk_ret['total'] * 1024)
	res['disk_read'] = long(disk_ret['read'] * 1024)
	res['disk_write'] = long(disk_ret['write'] * 1024)


	UtilsPlugin = plugin_manager.getPlugins(plugin_list[2])

	res['proNum'] = UtilsPlugin[0].processCount()
	res['Date'] = UtilsPlugin[0].getSysTime()
	res['occupiedPort'] = UtilsPlugin[0].getPorts()

	net_list = []
	NetPlugin = plugin_manager.getPlugins(plugin_list[3])
	for part in NetPlugin[0].extract():
		if part['name'] == 'bond0':
			net_list.append(copy.copy(part)) #deep copy
			break
		else:
			pass
	if len(net_list) != 0 and len(net_info) != 0:
		res['net_dev'] = net_list[0]['name']
		res['net_send'] = (net_list[0]['out'] - net_info[0]['out']) #bytes to bit *8/8
		res['net_recv'] = (net_list[0]['in'] - net_info[0]['in'])
	else:
		res['net_dev'] = 'bond0 device cannot find'
		res['net_send'] = ''
		res['net_recv'] = ''


	MemPlugins = plugin_manager.getPlugins(plugin_list[4])
	mem_ret = MemPlugins[0].extract()
	res['memSize'] = mem_ret['total']
	res['mem_used'] = mem_ret['total'] - mem_ret['free']
	res['mem_free'] = mem_ret['free']
	res['mem_buff'] = mem_ret['buffers']
	res['mem_cache'] = mem_ret['cached']

	try:
		server_address = os.getenv('SERVER_ADDRESS')
		if server_address:
			gelf_client = UdpClient(server_address.split(':')[0],server_address.split(':')[1])
		else:
			gelf_client = UdpClient()
		print "send successfully"
		gelf_client.send(res)
	except Exception, e:
		print e

	res = json.dumps(res,sort_keys=True,indent=4).encode('utf-8')
	print res

if __name__ == '__main__':
	try:
		while(1):
			perform(prepare())
	except Exception, e:
		print e
