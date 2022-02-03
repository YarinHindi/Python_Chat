import sys
import threading
import socket



nick_name = input('choose a nick_name >>>')
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('127.0.0.1', 55000))


def client_receive():
    connected = True
    bool_helper = True
    while connected:
        try:
            message = client_sock.recv(1024).decode('utf-8')
            # if str(message) == "b'"+nick_name+": Goodbye'":
            if str(message) == f'{nick_name}: Goodbye':
                print("Goodbye")
                client_sock.close()
                bool_helper = False
                break
            elif message == "nick?":
                client_sock.send(nick_name.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client_sock.close()
            exit(1)
            break



def client_send():
    connected = True
    while connected:
        c_input = input("")
        message = f'{nick_name}: {c_input}'
        client_sock.send(message.encode('utf-8'))
        if c_input == "exit":
            connected = False




receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
