from Tkinter import *
from threading import Thread
from Client import Client
import sys

class ClientUI:

    root=None

    name_label=None
    password_label = None


    connection_label=None
    log_listbox=None
    start_server_button=None

    message_entry=None
    send_button = None

    count=0
    client=None

    def __init__(self):
        self.root=Tk()
        self.connection_label=Entry(self.root,text="5006",width=100)
        self.connection_label.grid(row=0)
        self.connection_label.insert(0,"Enter the Port Number")


        self.name_label=Entry(self.root,text="Name",width=100)
        self.name_label.grid(row=1)
        self.name_label.insert(0,"Enter Your Name")

        self.password_label=Entry(self.root,text="Password",width=100)
        self.password_label.grid(row=2)
        self.password_label.insert(0,"Enter Your Password")

        Label(self.root,text="Log",width=100).grid(row=3)
        self.start_server_button=Button(self.root, text="Launch Client", width=100, command=self.on_start)
        self.log_listbox=Listbox(self.root,selectmode=EXTENDED,width=100)
        self.log_listbox.grid(row=4)

        self.start_server_button.grid(row=5)

        self.message_entry=Entry(self.root,text="",width=100)
        self.message_entry.grid(row=6)

        self.send_button=Button(self.root,text="Send",width=100,command=self.on_send)
        self.send_button.grid(row=7)

        self.root.mainloop()

    def append_message(self,message):
        self.count=self.count+1
        self.log_listbox.insert(self.count,message)
        
	

    def start_client(self):
        if((self.name_label != None) and (self.password_label != None) and (self.connection_label != None)):
            self.client = Client(self,self.name_label.get(),self.password_label.get(),'127.0.0.1',int(self.connection_label.get()))
        else:
            self.client= Client(self)
        self.client.chat()

    def on_send(self):
        self.client.send_message(self.message_entry.get())

    def on_start(self):
        thread = Thread(target=self.start_client)
        thread.start()
    
    def sigint_handler(signum, frame):
        sys.exit()


ClientUI()
