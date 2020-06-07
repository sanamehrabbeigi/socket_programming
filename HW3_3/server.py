import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random

COLOR = {
    'default': '\033[99m',
    'grey': '\033[90m',
    'green': '\033[92m',
    'magenta': '\033[95m',
    'white': '\033[97m',
    'red': '\033[91m'
}


def print_with_color(message, color='red'):
    print(COLOR.get(color.lower(), COLOR['default']) + message)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 12345))
    s.listen()
    print_with_color('Server Started Successfully','green')
except:
    print_with_color('problem with socket','red')

try:
    client, addr = s.accept()
    print_with_color('Client accepted Successfully','green')
except:
    print_with_color('problem with accepting client','red')

else:
    rnd = Random.new().read

    try:
        client_public_key = client.recv(2048)
        client_public_key = RSA.import_key(client_public_key)
        client_enc = PKCS1_OAEP.new(client_public_key)

        private_key = RSA.generate(1024, rnd)
        public_key = private_key.publickey()
        private_dec = PKCS1_OAEP.new(private_key)
        client.send(public_key.export_key())

        t = False # if t == true is server turn
        while True:
            if t == False :
                client_message = client.recv(1024)
                client_message = private_dec.decrypt(client_message).decode()
                print_with_color (client_message,'magenta')
                t = True
                if client_message == 'Good Bye':
                    print_with_color('Connection closed with Good Bye','gray')
                    client.close()
                    break

            else:
                try:
                    my_message = input()
                    data_enc = client_enc.encrypt(my_message.encode())
                    client.send(data_enc)
                    t = False
                    if my_message == 'Good Bye':
                        print_with_color('Connection closed with Good Bye', 'gray')
                        client.close()
                        break
                except ValueError:
                    print_with_color('Value Error!', 'red')
                    print_with_color('Please try again','white')
                    turn = True
                except KeyboardInterrupt:
                    print_with_color('Keyboard Interrupt Pressed', 'red')
                    s.close()
                    print_with_color('Connection Closed', 'red')
                    break
                except:
                    print_with_color('Error!','red')
                    s.close()
                    print_with_color('Connection Closed', 'red')
                    break


    except KeyboardInterrupt:
        print_with_color('Keyboard Interrupt Pressed','red')
        s.close()
        print_with_color('Connection Closed', 'red')

    s.close()
