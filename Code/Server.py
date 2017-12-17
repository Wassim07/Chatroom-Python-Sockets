import socket
import sys
import time
import threading
#from Cryptodome.Cipher import AES,DES
#from Cryptodome.Random import get_random_bytes
import _md5
import select
import signal
import Helpers



reload(sys)  # Reload does the trick!
sys.setdefaultencoding('iso-8859-1')


class Server:
    host = None
    port = None
    server_socket = None
    key='azertyuiopqsdfgh'
    sockets_list = []
    receiving_buffer = 4096  #the size of the buffer
    server_ui=None

    def __init__(self,ui,host="server",port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.sockets_list.append(self.server_socket)
        self.server_ui = ui
        self.server_ui.append_message("Server Started at Port : "+str(self.port))
        print("******************************\n     Server Started         \n******************************")

    def broadcast(self,server_socket, sock, message):
        for socket in self.sockets_list:

            if socket != server_socket and socket != sock:

                try:
                    socket.send(str.encode(message))
                except:
                    print("Error")
                    socket.close()

                    if socket in self.sockets_list:
                        self.sockets_list.remove(socket)

    def Main(self):
        while True:

            read_sockets, write_sockets, error_sockets = select.select(self.sockets_list, [], [])

            for sock in read_sockets:

                if sock == self.server_socket:
                    sockfd, addr = self.server_socket.accept()
                    self.sockets_list.append(sockfd)
                    self.server_ui.append_message('Got Connection from {} at {}\n'.format(addr,time.ctime(time.time())))
                    joining_msg = Helpers.Helpers.encrypt(self.key, "{}  has joined the chat room\n".format(addr))
                    str.encode(joining_msg)
                    self.broadcast(self.server_socket, sockfd,joining_msg )
                else:
                    try:
                        data = sock.recv(self.receiving_buffer)
                        data = Helpers.Helpers.decrypt(self.key, data)
                        if data:
                            self.broadcast(self.server_socket, sock, Helpers.Helpers.encrypt(self.key, "\r" + data))
                            self.server_ui.append_message(data.decode().lstrip())

                        else:

                            if sock in self.sockets_list:
                                self.sockets_list.remove(sock)
                                self.server_ui.append_message("User {} disconnected \n".format(addr))
                                self.broadcast(self.server_socket, sock, "User {} disconnected \n".format(addr))

                    except:
                        self.broadcast(self.server_socket, sock, "{} Shutdown!!!\n".format(addr))
                        self.server_socket.close()
                        continue



def sigint_handler(signum, frame):
    print ('\nUser disconnected !!')
    print ("\n\n")
    sys.exit()	
    
