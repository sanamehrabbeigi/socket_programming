import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1", 1234))

lst =[]

while True:
    data, addr = s.recvfrom(1024)
    data = data.decode()
    if ( data[:4] == 'POST'):
        lst.append((data[5:],addr))
    elif (data == 'GET' ):
        s.sendto(str(len(lst)).encode(), addr)
        for l in lst:
            s.sendto(str(l).encode(),addr)
        s.sendto("list end",addr)
    else:
        print("invalid request")


