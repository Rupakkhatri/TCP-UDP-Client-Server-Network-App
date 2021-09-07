########################################################################################################################
# Class: Computer Networks
# Date: 05/19/2021
# Final Project
# Student Name:Rupak Khatri
# Student ID:920605878
# Student Github Username:Rupakkhatri

########################################################################################################################
# copy and paste your server.py code from the labs
# don't modify this imports.
import socket
from threading import Thread
from clienthandler import ClientHandler


class Server(object):
    MAX_NUM_CONN = 10  # keeps 10 clients in queue

    def __init__(self, host="127.0.0.1", port=4545):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # your implementation for this socket here
        self.handlers = []  # initializes client_handlers list
        self.all_clients = []
        self.clients_active = []

        self.all_channels = []


    def _bind(self):
        self.server.bind((self.host, self.port))

    def check_client_status(self):
        while True:
            if False in self.clients_active:
                for i, s in enumerate(self.clients_active):
                    if s == False:
                        self.handlers.pop(i)
                        self.all_clients.remove(self.all_clients[i])
                        self.clients_active.pop(i)
                

    def _listen(self):
        self.server.listen(self.MAX_NUM_CONN)
        print(f"Server is running without issues\nListening at {self.host}/{self.port} ")

    def _accept_clients(self):
        while True:
            client, addr = self.server.accept()
            username = client.recv(1024).decode()
            userdata = [client, addr, username]

            self.all_clients.append(userdata)
            akn = f"Your client info is:\nClient Name: {username}\nClient ID: {addr[1]}"

            client.send(akn.encode()) # sending initial message to the client 
            thread = Thread(target=self._handler, args=(client, addr,username,))
            thread.start()

    def _handler(self, clienthandler, addr, username):
        client_hand = ClientHandler(self.server, clienthandler, addr, username, self.all_clients, self.all_channels)
        self.handlers.append(client_hand)

        def check_if_sending():
            while True:
                if client_hand.send_message != []:
                    if client_hand.send_message[2] == 'private':
                        message = client_hand.send_message[0]
                        recipient = client_hand.send_message[1]
                        for i in self.all_clients:
                            if i[1][1] == recipient:
                                recipient_handler = self.handlers[self.all_clients.index(i)]
                                recipient_handler.store_message_to_unread(message)
                    else:
                        message = client_hand.send_message[0]
                        for i in self.all_clients:
                            recipient_handler = self.handlers[self.all_clients.index(i)]
                            recipient_handler.store_message_to_unread(message)
                    
                    client_hand.send_message = []

        sending_thread = Thread(target=check_if_sending)
        sending_thread.start()
        self.clients_active.append(True)
        self.clients_active[len(self.clients_active)-1] = client_hand.run()
        

    def run(self):
        self._bind()
        self._listen()
        clients_thread = Thread(target=self.check_client_status)
        clients_thread.start()
        self._accept_clients()


# main execution
if __name__ == '__main__':
    server = Server()
    server.run()
