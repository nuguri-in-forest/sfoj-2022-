import socket
import socketserver
import json
import time
import hashlib
import struct
from os import system

import judger

PACKET_SALT = b"A8!nChS9"

'''
SFOJ Socket TCP Protocol Structure
-----------[NAME]----------[Value]---[BYTES]--
|  Check packet          |         |    8    |
----------------------------------------------
|   Dictionary Length    |         |    4    |
----------------------------------------------
|   JSON                 |         |    4    |
----------------------------------------------

[*] Dictionary Structure
- TYPE : JSON
- Content:
	LANG 					: C || CXX || Py ... # Submit Code Language
	SOURCE_CODE 			: code        # Submit Code
	TIME_LIMIT  			: time limit
	MEMORY_LIMIT 			: memory limit
	TMP_FILE_NAME           : random name

	(@TODO)Special Judge 	: @TODO

'''
class MyTCPHandler(socketserver.BaseRequestHandler):
	def gen_packet(self, ddict):
	    header = b""
	    header += hashlib.md5(ddict.encode()+PACKET_SALT).digest()[:8]
	    header += struct.pack("<I", len(ddict))
	    return header + ddict.encode()

	def handle(self):
		print("connect")
		sock = self.request

		Protocol_Header = sock.recv(12)
		"""
		hex(struct.unpack("<I", b"\x34\x12\x00\x00")[0])
		>>> '0x1234'
		"""
		print("protocol :", Protocol_Header)
		
		'''
		check packet
		'''
		SFOJ_CRC, Dic_len = Protocol_Header[:8], struct.unpack("<I", Protocol_Header[8:])[0]
		Dic = sock.recv(Dic_len)

		if SFOJ_CRC != hashlib.md5(Dic + PACKET_SALT).digest()[:8]:
			sock.send(gen_packet(json.dumps({}))) # empty json
			return -1

		Dic = json.loads(Dic)
		print(Dic)

		###### compile
		# create /tmp/TMP_FILE_NAME folder
		RunProcess = judger.RunningObject(Dic['TMP_FILE_NAME']) 				
		compile_OK = RunProcess.compile(Dic['LANG'], Dic['SOURCE_CODE'], Dic['TMP_FILE_NAME'])

		if compile_OK != 0:
			result = {'STATUS': '{"RESULT":{"1":"Compile Error"}, "SCORE":0}'}

			sock.send(self.gen_packet(json.dumps(result)))
			cmd = "rm -rf /tmp/%s*"%(Dic['TMP_FILE_NAME'])
			system(cmd)
			return

		###### running
		# def running(self, PROBLEM_ID, tmp_file_name, MEMORY_LIMIT, TIME_LIMIT, SPECIAL_JUDGE=0):
		Running_OK = RunProcess.running(Dic['PROBLEM_ID'], Dic['TMP_FILE_NAME'], Dic['MEMORY_LIMIT'], Dic['TIME_LIMIT']).strip()
		print("Running OK : ", Running_OK)

		###### TMP FILE Delete
		cmd = "rm -rf /tmp/%s*"%(Dic['TMP_FILE_NAME'])
		system(cmd)

		###### RESULT
		result = {"STATUS":Running_OK}
		
		# AVERAGE MEMORY, REAL_TIME ?? -> (@TODO) -> need to resource monitor..
		# result = {
		# 	"STATUS":Running_OK, # 0 -> Accept
		# 	"RESULT":[
		# 		{
		# 			"CPU_TIME":0,
		# 			"MEMORY":500,
		# 			"REAL_TIME":3,
		# 			"SIGNAL":0,
		# 			"OUTPUT_MD5":0
		# 		}
		# 	]
		# }
		sock.send(self.gen_packet(json.dumps(result)))

if __name__ == '__main__':
	HOST, PORT = "localhost", 12001

	socketserver.TCPServer.allow_reuse_address = True
	server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
	server.serve_forever()