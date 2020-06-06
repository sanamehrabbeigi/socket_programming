import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    print("what is your request? ")
    packet = input()
    s.sendto(packet.encode(),("127.0.0.1",1234))

    if packet == 'GET' :
            data, addr = s.recvfrom(1024)
            print("The list is : ")
            data_len = int(data)
            i =0
            for i in range(data_len):
                data,addr = s.recvfrom(1024)
                tp = data.encode()
                print (tp)

s.close()


