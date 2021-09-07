########################################################################################################################
# Class: Computer Networks
# Date: 05/19/2021
# Final Project
# Student Name:Rupak Khatri
# Student ID:920605878
# Student Github Username:Rupakkhatri

########################################################################################################################
import pickle, threading, socket


class ClientHelper:
    def __init__(self, client):
        self.client = client
        akr = self.client.recv(1024).decode()
        print(akr) # printing the initial message from the server(client Name and Id)
        self.id = int(akr.split("\n")[2].split(":")[1].strip())

    

    def send_request(self, request):
        self.client.send(pickle.dumps(request))

    def process_response(self):
        response = self.client.recv(1024)
        response = pickle.loads(response)
        return response

    def start(self):
        menu = pickle.loads(self.client.recv(12000))
        exec(menu, globals())
        udp_port = self.id
        menu = Menu(self.client, udp_port)
        while True:
            opt = menu.get()
            request = menu.options(opt)
            if request != None:
                self.send_request(request)
                print(self.process_response())