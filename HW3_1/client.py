from socket import *

#for IPv6 : AF_INET6  / localhost = ::1
s = socket(AF_INET, SOCK_STREAM)
s.connect(("127.0.0.1", 12345)) # or port : 12346
data = s.recv(1024)

if ( data.decode() == 'start') :
    num1 = input()
    num2 = input()
    s.send(str(num1).encode())
    s.recv(1024)
    s.send(str(num2).encode())
    sum = s.recv(1024)
    print("sum is : " + sum.decode())
else :
    print(data.decode())
s.close()