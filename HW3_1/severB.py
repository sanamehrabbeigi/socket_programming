import socket
import threading

#for IPv6 : AF_INET6  / localhost = ::1
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind(("127.0.0.1", 12345))
s2.bind(("127.0.0.1", 12346))
s1.listen(4)
s2.listen(4)

num_of_connect_clients = 0

def send_function(client):
    global num_of_connect_clients
    client.send(b'start')
    num1 = client.recv(1024)
    print(int(num1))
    client.send(b'ok')
    num2 = client.recv(1024)
    print(int(num2))
    sum = int(num1) + int(num2)
    print (sum)
    client.send(str(sum).encode())
    num_of_connect_clients -= 1


def accept_function(s):
    global num_of_connect_clients
    while True:
        client, addr = s.accept()
        if num_of_connect_clients < 4:
            #part c :
            #client.settimeout(10)
            num_of_connect_clients += 1
            t = threading.Thread(target=send_function, args=(client,))
            t.start()
        else:
            client.send(b'Server Is Busy')

t1 = threading.Thread(target=accept_function, args=(s1,))
t2 = threading.Thread(target=accept_function, args=(s2,))
t1.start()
t2.start()