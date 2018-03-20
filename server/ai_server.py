import socket
import threading
import Queue
import sys
import os

#ai api
from ai_celery_server import evaluate

lock = threading.Lock()
data_queue = Queue.Queue()
data_dict = {}
processing_data_dict = {}
socket_client_id = 0
socket_client = {}

def check_processing(data_url):
    lock.acquire()
    processing = processing_data_dict.has_key(data_url)
    lock.release()
    return processing

def set_processing(data_url):
    lock.acquire()
    processing_data_dict[data_url] = 1
    lock.release()

def remove_processing(data_url):
    lock.acquire()
    processing_data_dict.pop(data_url)
    lock.release()

def add_queue(data_url, user):
    # if check_processing(data_url):
    #     print('add processing data: %s' % data_url)
    #     return

    lock.acquire()

    if data_dict.has_key(data_url) :
        print('add repeated data: %s' % data_url)
        data_dict[data_url].append(user)
    else :
        data_dict[data_url] = []
        data_dict[data_url].append(user)
        data_queue.put(data_url)
        print('add queue: ', data_url)

    lock.release()

def pop_queue():
    data_url = data_queue.get()
    #users = data_dict.pop(data_url)
    print('pop queue: ', data_url)
    return data_url

def process_queue():
    print('process queue running.')
    while True:
        data_url = pop_queue()
        #set_processing(data_url)
        result = evaluate.delay(data_url)
        result.get()

        lock.acquire()
        users = data_dict.pop(data_url)
        lock.release()

        users_str = ''
        for i in range(len(users)):
            if i == len(users)-1:
                users_str += users[i]
            else:
                users_str += users[i] + ','    
        print('user: %s begin evaluate data: %s' % (users_str,data_url))
        #remove_processing(data_url)
        if socket_client.has_key('1'):
            socket_client['1'].send(users_str + '|' + data_url)

def console_echo():
    str = ''
    while True:
        str = raw_input()
        print(str)
        if str == 'close':
            print('close sys')
            os.kill()

def client_running(sock, addr, socket_client_id):
    print('Accept new connection from %s:%s...' % addr)
    while True:
        data = sock.recv(1024)
        if data == 'exit' or not data:
            break

        datas = data.split('|');
        user = datas[0]
        data_url = datas[1]
        print('user: %s begin evaluate data: %s' % (user,data_url))
        add_queue(data_url,user)
        
    sock.close()
    print 'Connection from %s:%s closed.' % addr 

def server_running():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 8005))
    s.listen(5)
    print ('waiting for connect...')
    while True:
        sock, addr = s.accept()
        global socket_client_id
        socket_client_id += 1
        socket_client[str(socket_client_id)] = sock
        print(socket_client)
        t = threading.Thread(target=client_running, args=(sock, addr, socket_client_id))
        t.start()
    

if __name__ == '__main__':
    ths = []
    for i in range(0,4):
        th = threading.Thread(target=process_queue)
        th.start()
        ths.append(th)
    th_echo = threading.Thread(target=console_echo)
    th_echo.start()

    server_running()
