import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random

COLOR = {
    'default': '\033[99m',
    'grey': '\033[90m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'white': '\033[97m',
    'red': '\033[91m'
}

def print_with_color(message, color):
    print(COLOR.get(color.lower(), COLOR['default']) + message)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 12345))
    print_with_color('Client Connected Successfully','green')
except ConnectionRefusedError:
    print_with_color('Cant Connect to Server', 'red')
    exit(0)
try:
    rnd = Random.new().read

    private_key = RSA.generate(1024, rnd)
    public_key = private_key.publickey()
    private_dec = PKCS1_OAEP.new(private_key)

    s.send(public_key.export_key())
    server_public_key = s.recv(2048)
    server_public_key = RSA.import_key(server_public_key)
    server_enc = PKCS1_OAEP.new(server_public_key)

    t = True  # if t == true is client turn
    while True:
        if t == True:
            try:
                my_message = input()
                data_enc = server_enc.encrypt(my_message.encode())
                s.send(data_enc)
                t = False
                if my_message == 'Good Bye':
                    print_with_color('Connection closed with Good Bye', 'grey')
                    s.close()
                    break
            except ValueError:
                print_with_color('Value Error!', 'red')
                print_with_color('Please try again', 'white')
                turn = True
            except KeyboardInterrupt:
                print_with_color('Keyboard Interrupt Pressed', 'red')
                s.close()
                print_with_color('Connection Closed', 'red')
                break
            except:
                print_with_color('Error!', 'red')
                s.close()
                print_with_color('Connection Closed', 'red')
                break

        else:
            server_message = s.recv(1024)
            server_message = private_dec.decrypt(server_message).decode()
            print_with_color(server_message, 'cyan')
            t = True
            if server_message == 'Good Bye':
                print_with_color('Connection closed with Good Bye', 'gray')
                s.close()
                break


except KeyboardInterrupt:
    print_with_color('Keyboard Interrupt Pressed', 'red')
    s.close()
    print_with_color('Connection Closed', 'red')

s.close()


