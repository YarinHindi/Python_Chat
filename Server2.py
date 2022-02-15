import threading

from client2 import Client2
import socket
import time


class Server:

    def __init__(self) -> None:
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind(('127.0.0.1', 55000))
        self.server_sock.listen(5)
        self.clients_map = {}
        self.clients_map_udp = {}
        self.file_names = []
        self.port_num = 50002
        self.ports = [0 for i in range(0, 15)]

    def send_files(self, nick_name):
        for i in self.file_names:
            self.clients_map.get(nick_name).client_sock.send(i.encode('utf-8'))


    def udp_transfer_files(self,nick_name,file_name):
        if self.clients_map_udp.get(nick_name) is None:
            for i in range(0, 15):
                if self.ports[i] == 0:
                    self.clients_map_udp[nick_name] = 50002 + i
                    self.ports[i] = 1
                    self.sent_to_other_user(nick_name, f'listen to port {self.clients_map_udp.get(nick_name)}'.encode('utf-8'))
                    time.sleep(0.02)
                    break
        print(self.ports)
        with open(file_name, 'rb') as f:
            content = f.read()
        print(str(content[0]))
        print(self.clients_map_udp.get(nick_name))
        self.server_sock_udp.sendto(content[0:1024], ('127.0.0.1', self.clients_map_udp.get(nick_name)))
        message, address = self.server_sock_udp.recvfrom(4096)
        print((message, address))

    def broadcast(self, message, nick_name):
        for nick, client in self.clients_map.items():
            if nick != nick_name:
                client.client_sock.send(message)

    def send_users(self, nick_name):
        for nick in self.clients_map:
            if nick != nick_name:
                self.clients_map[nick_name].client_sock.send(nick.encode('utf-8'))

    def sent_to_other_user(self, receiver, message_to):
        self.clients_map.get(receiver).client_sock.send(message_to)

    def handle_messages(self, nick_name):
        while True:
            try:
                bool = False
                message = self.clients_map[nick_name].client_sock.recv(1024).decode('utf-8')
                print(message)

                if message == f'{nick_name}: exit':
                    self.broadcast(f'{nick_name} has left the chat room'.encode('utf-8'), nick_name)
                    self.clients_map.get(nick_name).client_sock.send('Goodbye'.encode('utf-8'))
                    self.clients_map.pop(nick_name)
                    self.server_sock_udp.sendto('EXIT'.encode('utf-8'), ('127.0.0.1', self.clients_map_udp.get(nick_name)))
                    if self.clients_map_udp.get(nick_name) is not None:
                        self.ports[self.clients_map_udp.get(nick_name)-50002] = 0
                    break
                pure_message = message.split(": ")
                file_message = message.split(" ")
                send_to_message = str(pure_message).split("_")
                print(len(pure_message))
                if len(file_message) >= 3 and file_message[1] == "download_file":
                        file_name = file_message[2]
                        if file_name in self.file_names:
                            self.udp_transfer_files(nick_name, file_name)
                        else:
                            self.sent_to_other_user(nick_name, 'there is no such a file with that name'.encode('utf-8'))
                elif message == f'{nick_name}: get_file_names':
                    self.send_files(nick_name)
                elif pure_message[1] == "get_user_names":
                    print("porche?")
                    self.send_users(nick_name)
                elif len(send_to_message) >= 3:
                    meta = send_to_message[0].split(",")
                    # print(meta[1])
                    met_meta = meta[1][2:len(meta[1])]
                    print(met_meta)
                    print(send_to_message[1])
                    if met_meta == "send" and send_to_message[1] == "to":
                        print("inside")
                        meta_revciver = send_to_message[2].split()
                        recever = meta_revciver[0]
                        print(recever)
                        if self.clients_map.get(recever) is not None:
                            message_to = '' + str(nick_name) + ":" + str(
                                send_to_message[2][len(recever):len(send_to_message[2]) - 2])
                            self.sent_to_other_user(recever, message_to.encode())
                        else:
                            self.sent_to_other_user(nick_name, f'{recever} isnt in the room anymore'.encode('utf-8'))
                elif self.clients_map.get(nick_name) is not None:
                    self.broadcast(message.encode('utf-8'), nick_name)
                # else:
                #     self.broadcast(message.encode('utf-8'), nick_name)

            except:
                self.clients_map[nick_name].close()
                self.clients_map.pop(nick_name)
                break

    def receive(self):
        while True:
            print('Server is running and listening')
            client, adress = self.server_sock.accept()
            new_client = Client2()
            new_client.client_sock = client
            print(f'connection esatblish with {str(adress)}')
            client.send('nick?'.encode('utf-8'))
            nick_name = client.recv(1024).decode('utf-8')
            new_client.nick_name = nick_name
            # self.clients_map[nick_name] = client
            self.clients_map[nick_name] = new_client
            print(f' The nick_name of this client is {nick_name}')
            self.broadcast(f'{nick_name} has connected to the room'.encode('utf-8'), nick_name)
            client.send('you are connected'.encode('utf-8'))
            print(nick_name)
            tread = threading.Thread(target=self.handle_messages, args=(nick_name,))
            tread.start()


if __name__ == "__main__":
    server = Server()
    server.file_names.append("test.txt")
    server.file_names.append("another.txt")
    server.receive()
