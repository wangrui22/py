import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000))

while True:
    a = raw_input('input command: ')
    if not a:
        break
    
    u = a.encode('utf-8')
    print('input context: ', u)
    s.send(u)
    
    echo_back = s.recv(1024)
    print(echo_back.decode('utf-8'))

s.close()