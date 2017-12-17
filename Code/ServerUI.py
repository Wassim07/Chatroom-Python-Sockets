from Tkinter import *
from threading import Thread
from Server import Server
import sys


reload(sys)  # Reload does the trick!
sys.setdefaultencoding('iso-8859-1')


class ServerUI:

    root=None
    connection_label=None
    start_server_button=None
    log_listbox=None
    count=0
    server=None
    def __init__(self):
        self.root=Tk()
        self.connection_label=Entry(self.root,text="5000",width=100)
        self.connection_label.grid(row=0)
        self.connection_label.insert(0,"5000")
        Label(self.root,text="Log",width=100).grid(row=1)
        self.start_server_button=Button(self.root, text="Launch Server", width=100, command=self.on_start)
        self.log_listbox=Listbox(self.root,selectmode=EXTENDED,width=100)
        self.log_listbox.grid(row=2)
        self.start_server_button.grid(row=3)
        self.root.mainloop()

    def append_message(self,message):
        self.count=self.count+1
        self.log_listbox.insert(self.count,message)
        
	
    def start_server(self):
        if(self.connection_label != None):
            self.server = Server(self,'127.0.0.1',int(self.connection_label.get()))
        else:
            self.server = Server(self)
        self.server.Main()


    def on_start(self):
        thread = Thread(target=self.start_server)
        thread.start()


    
    def sigint_handler(signum, frame):
        print ('\n User disconnected !!')
        print ("\n\n")
        sys.exit()	


ServerUI()
