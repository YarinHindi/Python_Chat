import threading
import socket

host = '127.0.0.1'

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind(('127.0.0.1', 55000))
server_sock.listen(5)
clients_map = {}


def broadcast(message, nick_name):
    for nick, client in clients_map.items():
        if nick != nick_name:
            client.send(message)


def send_users(nick_name):
    for nick in clients_map:
        if nick != nick_name:
            clients_map[nick_name].send(nick.encode('utf-8'))


def sent_to_other_user(receiver, message_to):
    receiver.send(message_to)


def handle_messages(nick_name):
    while True:
        try:
            bool = False
            message = clients_map[nick_name].recv(1024).decode('utf-8')

            # if str(message) == "b'"+nick_name+": exit'":
            # if str(message) == f"b'{nick_name}: exit":
            if message == f'{nick_name}: exit':
                broadcast(f'{nick_name} has left the chat room'.encode('utf-8'), nick_name)
                clients_map.get(nick_name).send('Goodbye'.encode('utf-8'))
                clients_map.pop(nick_name)
                break

            string_messgee = ''+str(message)
            pure_message = str(message).split(": ")
            send_to_message = str(pure_message).split("_")
            print(pure_message[1])
            # print(send_to_message[0])
            # print(send_to_message[1])
            if pure_message[1] == "get_user_names":
                send_users(nick_name)
            elif len(send_to_message) >= 3:
                meta = send_to_message[0].split(",")
                # print(meta[1])
                met_meta = meta[1][2:len(meta[1])]
                # print(met_meta)
                if met_meta=="send" and send_to_message[1]=="to":
                    print("inside")
                    meta_revciver = send_to_message[2].split()
                    recever = meta_revciver[0]
                    message_to = ''+str(nick_name)+":"+str(send_to_message[2][len(recever):len(send_to_message[2])-2])
                    sent_to_other_user(clients_map.get(recever), message_to.encode())
            elif clients_map.get(nick_name) is not None:
                broadcast(message.encode('utf-8'), nick_name)
        except:
            clients_map[nick_name].close()
            clients_map.pop(nick_name)
            break


def receive():
    while True:
        print('Server is running and listening')
        client, adress = server_sock.accept()
        print(f'connection esatblish with {str(adress)}')
        client.send('nick?'.encode('utf-8'))
        nick_name = client.recv(1024).decode('utf-8')
        # nick_names.append(nick_name)
        # clients.append(client)
        # map_nick = str(nick_name).split("'")[1]
        clients_map[nick_name] = client
        print(f' The nick_name of this client is {nick_name}')
        broadcast(f'{nick_name} has connected to the room'.encode('utf-8'), nick_name)
        client.send('you are connected'.encode('utf-8'))
        tread = threading.Thread(target=handle_messages, args=(nick_name,))
        tread.start()



if __name__ == "__main__":
    receive()

