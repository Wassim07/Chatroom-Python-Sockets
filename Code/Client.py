import socket
import sys
import select
import time
import Helpers

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('iso-8859-1')
#10
class Client:
    alias = None
    server = None
    socket = None
    key=''
    client_ui=None



#20
    def __init__(self,ui, host="user", port=5000):
        self.client_ui=ui
     
        self.alias = input("Enter you name : ")
        self.key = input("Enter you password : ")

        self.server = (host,port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
#30

    def __init__(self,ui, name="",key="",host="127.0.0.1", port=5000):
        self.client_ui=ui

        self.alias = name
        self.key = key


        self.server = (host,port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
#42        
	
    def connect_to_server(self):
        try:
            self.socket.connect(self.server) #Connecting

            self.client_ui.append_message("You've Joined the chat room successfully at {}\n".format(time.ctime(time.time())))#append_message etant une simple methode pour afficher une nouvelle ligne
#48
            sys.stdout.write("You've Joined the chat room successfully at {}\n".format(time.ctime(time.time())))#On signale que l'utilisateur s'est bel et bien co..
            sys.stdout.write("\033[36m" + '\n[Me :] ' + "\033[0m");
            sys.stdout.flush()
        except:
            print('Unable to connect')
            sys.exit()


#this method will be triggered when the user click on the send button
    def send_message(self,msg):
        #preparing the message format
        msg = '[ ' + self.alias + ' ] : ' + msg

        self.client_ui.append_message(msg)

        #encrypting
        msg = Helpers.Helpers.encrypt(self.key,msg)
        #encoding the message , default encoding : iso-8859-1
        msg=str.encode(msg)
        self.socket.send(msg)

    def chat(self):
        self.connect_to_server()

        while True:
            socket_list = [sys.stdin, self.socket]
            read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

            for sock in read_sockets:
#we only care about the socket that was created between the server and the client
                if sock == self.socket:

                    data = sock.recv(4096)

                    if not data:
                        print
                        "\nServer shutdown !!"
                        sys.exit()
                    else:
#decrypting the received message
                        data = Helpers.Helpers.decrypt(self.key, data)

#printing it after decoding it , default encoding : iso-8859-1)
                        self.client_ui.append_message("\n"+data.decode().lstrip())


                else:
#this will be printed on the console , it's the same as send_message
                    msg = sys.stdin.readline()
                    msg = '[ ' + self.alias + ' ] : ' + msg
                    msg = Helpers.Helpers.encrypt(self.key,msg)
                    self.socket.send(str.encode(msg))


def sigint_handler(signum, frame):
    print ('\n User disconnected !!')
    print ("\n\n")
    sys.exit()	
    

