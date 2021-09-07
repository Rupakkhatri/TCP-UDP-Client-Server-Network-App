########################################################################################################################
# Class: Computer Networks
# Date: 05/19/2021
# Final Project
# Student Name:Rupak Khatri
# Student ID:920605878
# Student Github Username:Rupakkhatri

########################################################################################################################
import os


class Menu(object):
    def __init__(self, handler, udp_port):
        self.menu = """
****** TCP/UDP Network ******
------------------------------------
Options Available:
1.  Get users list
2.  Send a message
3.  Get my messages
4.  Send a direct message with UDP protocol
5.  Broadcast a message with CDMA protocol
6.  Create a secure channel to chat with your friends using PGP protocol
7.  Join an existing channel
8.  Create a Bot to manage a future channel
9.  Map the network
10.  Get the Routing Table of this client with Link State Protocol
11. Get the Routing Table of this network with Distance Vector Protocol
12. Turn web proxy server on (extra-credit)
13. Disconnect from server"""
        self.handler = handler
        self.udp_message = []

        udp_thread = threading.Thread(target= self.udp_receiver, args=(udp_port,))
        udp_thread.start()

    def send(self,data):
        data = pickle.dumps(data)
        self.handler.send(data)

    def receive(self):
        data = self.handler.recv(1024)
        data = pickle.loads(data)
        return data

    def udp_receiver(self, udp_port):
        udp_receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_receiver_socket.bind(('0.0.0.0', udp_port))
        while True:
            message, sender_addr = udp_receiver_socket.recvfrom(1024)
            message = pickle.loads(message)
            message = f"UDP Message from {sender_addr} : {message}"
            self.udp_message.append(message)

    def get(self):
        while True:
            for i in self.udp_message:
                print(i)
            self.udp_message = []
            print(self.menu)
            try:
                opt = int(input("\nYour option <enter a number>: "))
                return opt

            except:
                print("\nPlease Enter a Number!!\n")

    def options(self, opt):

        def opt_1():
            return {"option":1}
        def opt_2():
            message = input("Enter your message: ")
            while True:
                try:
                    recipient = int(input("Enter recipient id: "))
                    break
                except:
                    print("Recepient id should be a number!!")
            return {"option":2, "message":message, "recipient":recipient}
        def opt_3():
            return {"option":3}
        def opt_4():
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while True:
                try:
                    bind_addr = input("Enter the address to bind your UDP client (e.g 127.0.0.1:6000): ")
                    ip = bind_addr.split(":")[0]
                    port = int(bind_addr.split(":")[1])
                    udp_socket.bind((ip,port))
                    break
                except:
                    print("Can't bind with this address!!")
            while True:
                try:
                    recipient_addr = input("Enter the recipient address: ")
                    recipient_addr = recipient_addr.split(":")
                    recipient_addr = (recipient_addr[0], int(recipient_addr[1]))
                    break
                except:
                    print("Invalid Address!!")
            

            message = input("Enter the message: ")
            message = pickle.dumps(message)
            udp_socket.sendto(message, recipient_addr)
            udp_socket.close()
            print(f"UDP client running and accepting other clients at udp {ip}:{port}")
            print(f"Message sent to udp address: {recipient_addr[0]}:{recipient_addr[1]}")
            return None

        def opt_5():
            message = input("Enter the message: ")
            return {"option":5,"message":message}
        def opt_6():
            while True:
                while True:
                    try:
                        channel_id = int(input("Enter the new channel id: "))
                        break
                    except:
                        print("Channel ID should be a number")
                self.send({"option":6,"channel_id":str(channel_id)})
                req = self.receive()
                print(req[0])
                if req[1] != False:
                    break
            self.stop_7 = True
            def recv_6():
                while self.stop_7:
                    mesg = self.receive()
                    print(mesg)
                    if mesg[1] == 0:
                        self.stop_7 = False
            recv_thread = threading.Thread(target=recv_6)
            recv_thread.start()
            while self.stop_7:
                mesg = input()
                self.send(mesg)
                if mesg == "#exit":
                    self.stop_7 = False
            #recv_thread.join()
            return None
        def opt_7():
            chn_id = input("Enter channel id you'd like to join: ")
            self.send({"option":7,"channel_id":chn_id})
            resp = self.receive()
            print(resp[0])
            if resp[1] == False:
                return None

            self.stop_6 = True
            def recv_6():
                while self.stop_6:
                    mesg = self.receive()
                    print(mesg[0])
                    if mesg[1] == 0:
                        self.stop_6 = False
            recv_thread = threading.Thread(target=recv_6)
            recv_thread.start()
            while self.stop_6:
                mesg = input()
                self.send(mesg)
                if mesg == "#bye":
                    recv_thread.join()
                    self.stop_6 = False
                    break
            return None
            
        def opt_8():
            pass
        def opt_9():
            return {"option":9}
        def opt_10():
            return {"option":10}
        def opt_11():
            return {"option":11}
        def opt_12():
            pass
        def opt_13():
            os._exit(0)

        options_list = [opt_1, opt_2, opt_3, opt_4, opt_5, opt_6, opt_7, opt_8,opt_9, opt_10, opt_11, opt_12, opt_13]

        req = options_list[opt-1]()
        return req

