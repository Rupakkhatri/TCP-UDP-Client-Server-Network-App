########################################################################################################################
# Class: Computer Networks
# Date: 05/19/2021
# Final Project
# Student Name:Rupak Khatri
# Student ID:920605878
# Student Github Username:Rupakkhatri

########################################################################################################################
import pickle, time
from datetime import datetime
from tabulate import tabulate


class ClientHandler:

    def __init__(self, server_instance, clienthandler, addr, username, current_active_clients, all_channels):
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.username = username
        self.server = server_instance
        self.handler = clienthandler
        self.unread_messages = []
        self.all_clients = current_active_clients
        self.all_channels = all_channels
        self.send_message = []
        self.channel = ""
        menu_file = open('menu.py', 'r').read()
        self.send(menu_file)

    def send(self, data):
        data = pickle.dumps(data)
        self.handler.send(data)

    def receive(self, max_mem_alloc=1024):
        request = self.handler.recv(max_mem_alloc)
        deserialized_data = pickle.loads(request)
        return deserialized_data

    def process_request(self):
        while True:
            try:
                request = self.receive()
                print(request)
                self.analyze_request(request)
            except:
                break

    def send_message_to_server(self, message):
        return message

    def analyze_request(self, request):
        def opt_1():
            reply = f"Users connected: {len(self.all_clients)}\n"
            for i in self.all_clients:
                id = i[1][1]
                username = i[2]
                if id == self.client_id:
                    username = "You"
                if self.all_clients.index(i) == 0:
                    reply += f"{username}:{id}"
                    continue
                reply += f", {username}:{id}"

            self.send(reply)

        def opt_2():
            message = request["message"]
            recipient = request["recipient"]
            all_recipient = [i[1][1] for i in self.all_clients]
            if recipient not in all_recipient:
                self.send(f"Recipient with {recipient} not found!!")
            else:
                mesg = datetime.now().strftime("%Y-%m-%d %H:%M:")
                mesg += " " + message
                mesg += f" (private message from {self.username})"
                self.send_message = [mesg, recipient, "private"]
                self.send("Message sent!")

        def opt_3():
            reply = f"Number of unread messages: {len(self.unread_messages)}\n"
            for um in self.unread_messages:
                reply += '\n'+um
            self.send(reply)
            self.unread_messages = []

        def opt_5():
            message = request["message"]
            mesg = datetime.now().strftime("%Y-%m-%d %H:%M:")
            mesg += " " + message
            mesg += f" (broadcast message from {self.username})"
            self.send_message = [mesg, None, "broadcast"]
            self.send("Message broadcast!")

        def opt_6():
            self.check_channel = True
            time.sleep(0.1) # this is for giving time for the server to authorize the channel
            self.channel = request["channel_id"]

            if self.channel in [i[1] for i in self.all_channels]:
                self.send([f"Channel with Id --> {self.channel} is found!!\nTry Another.", False])
            else:
                msg = f"Private key received from server and channel {self.channel} was successfully created!\n\n"
                msg += f"----------------------- Channel {self.channel} ------------------------\n\n"
                msg += "All the data in this channel is encrypted\n\n"
                msg += "General Admin Guidelines:\n"
                msg += f"1. #{self.username} is the admin of this channel\n"
                msg += "2. Type '#exit' to terminate the channel (only for admins)\n\n\n"
                msg += "General Chat Guidelines:\n"
                msg += "1. Type #bye to exit from this channel. (only for non-admins users)\n"
                msg += "2. Use #<username> to send a private message to that user.\n\n"
                msg += "Waiting for other users to join...."
                self.send([msg, True])
                self.all_channels.append([self.username,self.channel, []])

                def recv():
                    s = True
                    while s:
                        data = self.receive()
                        
                        if data[0] == "#":
                            if data == "#exit":
                                data = [f"Channel {self.channel} closed by admin.", 0]
                                data = pickle.dumps(data)
                                for i in self.all_clients:
                                    if i[2] != self.username:
                                        client = i[0]
                                        client.send(data)
                                s = False
                                chn = [i[1] for i in self.all_channels].index(self.channel)
                                chn = self.all_channels[chn]
                                self.all_channels.remove(chn)
                                break
                            else:
                                username = ""
                                for i in data[1:]:
                                    if i == " ":
                                        break
                                    username += i
                                all_usernames = [i[2] for i in self.all_clients]
                                if username in all_usernames:
                                    data = [data, 1]
                                    data = pickle.dumps(data)
                                    recp_user = self.all_clients[all_usernames.index(username)][0]
                                    recp_user.send(data)
                        else:
                            data = [data, 1]
                            data = pickle.dumps(data)
                            for i in self.all_clients:
                                if i[2] != self.username:
                                    client = i[0]
                                    client.send(data)
                            
                recv()

        def opt_7():
            self.channel = request["channel_id"]
            if self.channel not in [i[1] for i in self.all_channels]:
                self.send([f"Channel with channel id {self.channel} is not found!",False])
            else:
                other_clients = self.all_channels[[i[1] for i in self.all_channels].index(self.channel)][2]
                
                chan = self.all_channels[[i[1] for i in self.all_channels].index(self.channel)]
                msg = f"----------------------- Channel {self.channel} ------------------------\n\n"
                msg += "All the data in this channel is encrypted\n\n"
                msg += f"{self.username} just joined\n"
                if len(other_clients) > 1:
                    last_client = other_clients[-1]
                    other_clients = ", ".join(other_clients[:len(other_clients)-1])
                    other_clients += f" and {last_client}"
                    msg += f"{other_clients} are already on the channel"
                msg += f"{chan[0]} is the admin of this channel\n\n"
                print("6")
                msg += "General Chat Guidelines:\n"
                msg += "1. Type #bye to exit from this channel. (only for non-admins users)\n"
                msg += "2. Use #<username> to send a private message to that user.\n"
                self.send([msg, True])
                self.all_channels[[i[1] for i in self.all_channels].index(self.channel)][2].append(self.username)
                
                while True:
                    data = self.receive()
                    
                    if data[0] == "#":
                        if data == "#bye":
                            break
                        else:
                            username = ""
                            for i in data[1:]:
                                if i == " ":
                                    break
                                username += i
                            all_usernames = [i[2] for i in self.all_clients]
                            if username in all_usernames:
                                data_pic = [data, 1]
                                data_pic = pickle.dumps(data_pic)
                                recp_user = self.all_clients[all_usernames.index(username)][0]
                                recp_user.send(data_pic)
                    else:
                        data_pic = [data, 1]
                        data_pic = pickle.dumps(data_pic)
                        for i in self.all_clients:
                            if i[2] != self.username:
                                client = i[0]
                                client.send(data_pic)

        def opt_8():
            pass

        def opt_9():
            str = "\n\nRouting table requested! Waiting for response.... \n\nNetwork Map:\n\n"
            lis = []
            printable_table = []
            name_row = [""]
            for val in self.all_clients:
                val = val[2]
                name_row.append(val)
                lis.append(val)
            printable_table.append(name_row)
            rows, cols = (len(self.all_clients),len(self.all_clients))
            arr = [[-9 for i in range(cols)] for j in range(rows)]
            for i in range(0, rows):
                arr[i][i] = 0
            v = 1
            for i in range(0, rows):
                rows = [lis[i]]
                for j in range(0, cols):
                    if arr[i][j] == -9:
                        arr[i][j] = v
                        arr[j][i] = v
                        v += 1
                    rows.append(arr[i][j])
                printable_table.append(rows)
            table = tabulate(printable_table, headers='firstrow')
            str += table
            self.send(str)

        def opt_10():
            str = "\n\nRouting table requested! Waiting for response.... \n\nNetwork Map:\n\n"
            lis = []
            printable_table = []
            name_row = [""]
            for val in self.all_clients:
                val = val[2]
                name_row.append(val)
                lis.append(val)
            printable_table.append(name_row)
            rows, cols = (len(self.all_clients),len(self.all_clients))
            arr = [[-9 for i in range(cols)] for j in range(rows)]
            for i in range(0, rows):
                arr[i][i] = 0
            v = 1
            for i in range(0, rows):
                row = [lis[i]]
                for j in range(0, cols):
                    if arr[i][j] == -9:
                        arr[i][j] = v
                        arr[j][i] = v
                        v += 1
                    row.append(arr[i][j])
                printable_table.append(row)
            table = tabulate(printable_table, headers='firstrow')
            str += table
            printable_table = []
            id_lis = [i[1][1] for i in self.all_clients]
            ind = id_lis.index(self.client_id)
            str += f"\n\nRouting table for {self.username} (id: {self.client_id}) computed with Link State Protocol: \n\n"
            firstrow = ["destination", "Path", "Cost"]
            printable_table.append(firstrow)
            for i in range(0, rows):
                row = []
                if i==ind:
                    continue
                cost=0
                row.append(lis[i])
                s = "("
                for j in range(0, j):
                    s += f"{lis[j]},"
                    cost += arr[ind][j]
                
                s += ")"
                row.append(s)
                row.append(cost)
                printable_table.append(row)

            second_table = tabulate(printable_table, headers='firstrow')
            str += second_table
            self.send(str)

        def opt_11():

            str = "\n\nRouting table requested! Waiting for response.... \n\nNetwork Map:\n\n"
            lis = []
            printable_table = []
            name_row = [""]
            for val in self.all_clients:
                val = val[2]
                name_row.append(val)
                lis.append(val)
            printable_table.append(name_row)
            rows, cols = (len(self.all_clients),len(self.all_clients))
            arr = [[-9 for i in range(cols)] for j in range(rows)]
            for i in range(0, rows):
                arr[i][i] = 0
            v = 1
            for i in range(0, rows):
                row = [lis[i]]
                for j in range(0, cols):
                    if arr[i][j] == -9:
                        arr[i][j] = v
                        arr[j][i] = v
                        v += 1
                    row.append(arr[i][j])
                printable_table.append(row)
            table = tabulate(printable_table, headers='firstrow')
            str += table
            str += f"\n\nRouting table for {self.username} (id: {self.client_id}) computed with Distance Vector Protocol: \n\n"
            lis = []
            printable_table = []
            name_row = [""]
            for val in self.all_clients:
                val = val[2]
                name_row.append(val)
                lis.append(val)
            printable_table.append(name_row)
            rows, cols = (len(self.all_clients),len(self.all_clients))
            arr = [[-9 for i in range(cols)] for j in range(rows)]
            for i in range(0, rows):
                arr[i][i] = 0
            v = 1
            for i in range(0, rows):
                row = [lis[i]]
                for j in range(0, cols):
                    if arr[i][j] == -9:
                        arr[i][j] = v
                        arr[j][i] = v
                        v += 1
                    row.append(arr[i][j])
                printable_table.append(row)
            table = tabulate(printable_table, headers='firstrow')
            str += table
            self.send(str)

        def opt_12():
            pass

        def opt_13():
            pass
        
        opt = request['option']
        self.options_list = [opt_1, opt_2, opt_3, None, opt_5, opt_6, opt_7, opt_8, opt_9, opt_10, opt_11, opt_12, opt_13]

        self.options_list[opt-1]()


    def store_message_to_unread(self, message):
        self.unread_messages.append(message)

    def run(self):
        self.process_request()
        return False # this returns when the client leaves the server!

    
