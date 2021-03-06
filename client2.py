import sys
import threading
import socket
import time


class Client2:
    connected = True
    def __init__(self, nick_name=0) -> None:
        self.nick_name = nick_name
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)



    def udp_handler(self, port_num):

        self.client_sock_udp.bind(('127.0.0.1', port_num))
        while True:
            message, address = self.client_sock_udp.recvfrom(4096)
            if message.decode('utf-8') == 'EXIT':
                break
            file = open("file_name.txt", 'wb')
            file.write(message)
            print(message.decode('utf-8'))
            print(address)
            file.close()
            self.client_sock_udp.sendto('got the file thanks'.encode('utf-8'), address)


    def choose_nick_name(self):
        self.nick_name = input('choose a nick_name >>>')

    def client_receive(self):
        connected = True
        bool_helper = True
        while True:
            if not self.connected:
                break
            try:
                message = self.client_sock.recv(1024).decode('utf-8')
                if str(message) == f'{self.nick_name}: Goodbye':
                    print("Goodbye")
                    connected = False
                    self.client_sock.close()
                    self.client_sock_udp.close()
                elif message == "nick?":
                    self.client_sock.send(self.nick_name.encode('utf-8'))
                elif len(message) >= 14 and message[0:14] == "listen to port":
                    port_num = message[15:len(message)]
                    print(port_num)
                    receive_udp_thread = threading.Thread(target=self.udp_handler, args=(int(port_num),))
                    receive_udp_thread.start()
                else:
                    print(message)
            except:
                print('Error!')
                self.client_sock.close()
                exit(1)
                break

    def client_conncet(self):
        self.client_sock.connect(('127.0.0.1', 55000))
        receive_thread = threading.Thread(target=self.client_receive)
        receive_thread.start()
        send_thread = threading.Thread(target=self.client_send)
        send_thread.start()

    def client_send(self):
        while self.connected:
            c_input = input("")
            message = f'{self.nick_name}: {c_input}'
            self.client_sock.send(message.encode('utf-8'))
            if c_input == "exit":
                self.connected = False

if __name__ == '__main__':
    client = Client2()
    client.choose_nick_name()
    client.client_conncet()

