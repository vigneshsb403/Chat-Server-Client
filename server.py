#!/usr/bin/env python3
import socket
import sys
import select
HOST=''; PORT= 4444
SOCKET_LIST=[]
RECIVE_BUFFER= 4096
def chat_server():
	server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST,PORT))
	server_socket.listen()
	SOCKET_LIST.append(server_socket)
	print("Chat server is listening on port {}...".format(PORT))
	while True:
		ready_read,ready_write, error = select.select(SOCKET_LIST,[],[],0)
		for sock in ready_read:
			if sock == server_socket:
				client_socket,addr=server_socket.accept()
				SOCKET_LIST.append(client_socket)
				print("Client {}:{} connected...".format(addr[0], addr[1]))
				broadcast(server_socket,client_socket,"{} entered our chatting room... \n".format(addr))
			else:
				try:
					data=sock.recv(RECIVE_BUFFER)
					if data:
						broadcast(server_socket,sock, "[{}] {}".format(sock.getpeername(),data))
					else:
						broadcast(server_socket,sock, "[{}] {}".format(sock.getpeername(),"client is offline \n"))
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock)
				except:
					broadcast(server_socket, sock,"[{}] {}".format(sock.getpeername(),"client is offline"))
	def broadcast(server_socket,client_socket,message):
		for socket in SOCKET_LIST:
			if socket != server_socket and socket != client_socket:
				try:
					socket.sendmsg(message)
				except:
					socket.close()
					if socket in SOCKET_LIST:
						SOCKET_LIST.remove(socket)
if __name__ == "__main__":
	sys.exit(chat_server())
