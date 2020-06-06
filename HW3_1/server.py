import socket
import threading

#for IPv6 : AF_INET6  / localhost = ::1
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127 .0.0.1", 12345))
s.listen(4)

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
