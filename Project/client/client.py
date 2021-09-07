########################################################################################################################
# Class: Computer Networks
# Date: 05/19/2021
# Final Project
# Student Name:Rupak Khatri
# Student ID:920605878
# Student Github Username:Rupakkhatri

########################################################################################################################
import socket
import pickle
from clienthelper import ClientHelper

class Client(object):

    def __init__(self, username):
        """
        Class constructor
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = username

    def connect(self, server_ip_address, server_port):
        try:
            self.client.connect((server_ip_address, server_port))
            print(f"Successfully connected to server: {server_ip_address}/{server_port}")
            self.client.send(self.username.encode()) # sending the username to the server
        except:
            print("Server is not available :(")

    def client_helper(self):
        client_helper = ClientHelper(self.client)
        client_helper.start()

    def close(self):
        self.client.close()


# main code to run client
if __name__ == '__main__':
    server_ip = input("Enter the server IP Address: ")
    while True:
        try:
            server_port =int( input("Enter the server port: "))
            break
        except:
            print("PORT SHOULD BE A NUMBER!!")
    username = input("Enter a username: ")
    client = Client(username)
    client.connect(server_ip, server_port)  # creates a connection with the server
    client.client_helper()
