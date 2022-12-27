#!/usr/bin/env python3
import sys
import socket
import select

SOCKET_LIST=[sys.stdin]

def chat_client():
	if len(sys.argv)<3:
		print("Usage: python3 {} hostname port".format(sys.argv[0]))
	host=sys.argv[1]
	port=int(sys.argv[2])
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.settimeout(5)
	
	try:
		s.connect((host,port))
	except:
		print("[!]:Warning {}:{} is not up...".format(host,port))
		sys.exit(-1)

	print("[#]:Info Connected to remote host...")
	print("[#]:Info You can send packets...")
	#print(">^:: ",end='')
	sys.stdout.write(">^:: ")
	sys.stdout.flush()
	
	while True:
		ready_read,ready_write, error = select.select(SOCKET_LIST,[],[])
		for sock in ready_read:
			if sock == s:
				data=data.recv(4096)
				if not data:
					print("[*]:Error Chat disconected")
					sys.exit(-1)
				else:
					sys.stdout.write(data)   # do not use print as it would block the stream
					sys.stdout.write(">^:: ")
					sys.stdout.flush()
			else:
				msg=sys.stdin.readline()
				s.send(msg.encode())
				sys.stdout.write(">^:: ")
				sys.stdout.flush()

if __name__ == "__main__":
	sys.exit(chat_client())
	