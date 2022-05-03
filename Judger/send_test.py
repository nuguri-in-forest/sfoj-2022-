import json
import random
import hashlib
import struct
import socket
import base64

HOST = 'localhost'
PORT  = 12001

test_json = {
	"LANG":"C",
	"SOURCE_CODE":"""#include<stdio.h>

int main(void)
{
	printf("Hello World!\\n");
	return 0;
}""",
	"TIME_LIMIT":1000,
	"MEMORY_LIMIT":1000,
}
test_json['TMP_FILE_NAME'] = hashlib.md5(test_json['SOURCE_CODE'].encode()).hexdigest()


PACKET_SALT = b"A8!nChS9"
def gen_packet(ddict):
    header = b""
    header += hashlib.md5(ddict.encode()+PACKET_SALT).digest()[:8]
    header += struct.pack("<I", len(ddict))
    return header + ddict.encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))
    
    s.send(gen_packet(json.dumps(test_json)))

    s.close()