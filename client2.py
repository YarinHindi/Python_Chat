import sys
import threading
import socket


class Client2:
    connected = True
    def __init__(self, nick_name=0) -> None:
        self.nick_name = nick_name
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

                elif message == "nick?":
                    self.client_sock.send(self.nick_name.encode('utf-8'))
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
