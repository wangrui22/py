import SocketServer
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
tcp_client = None

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

def add_queue(data_url,user):
    
    if check_processing(data_url):
        print('add processing data: %s' % data_url)
        return

    if data_dict.has_key(data_url) :
        data_dict[data_url] += 1
    else :
        data_dict[data_url] = 1
        data_queue.put(data_url)

    print('add queue: ', data_url)

def pop_queue():
    data_url = data_queue.get()
    data_dict.pop(data_url)
    print('pop queue: ', data_url)
    return data_url

def process_queue():
    print('process queue running.')
    while True:
        data_url = pop_queue()
        set_processing(data_url)
        result = evaluate.delay(data_url)
        print('data: ', data_url, 'process done, ' , result.get())
        remove_processing(data_url)
        tcp_client.sendall(data_url.decode('utf-8')) 

# just consider one client 
class AIServer(SocketServer.BaseRequestHandler):
    def handle(self):
        print('AI TCP server start...')
        conn = self.request
        print('get connection:', self.client_address)
        while True:
            data_url = conn.recv(1024)
            if not data_url:
                print('empty data url.')
                continue
            data = data_url.decode('utf-8')
            datas = data.split('|');
            user = datas[0]
            data_url = datas[1]
            print('user: %s begin evaluate data: %s' % (user,data_url))
            add_queue(data_url, user)
            # push request to queue
            
def console_echo():
    str = ''
    while True:
        str = raw_input()
        print(str)
        if str == 'close':
            print('close sys')
            os.kill()
            

if __name__ == '__main__':
    ths = []
    for i in range(0,4):
        th = threading.Thread(target=process_queue)
        th.start()
        ths.append(th)
    th_echo = threading.Thread(target=console_echo)
    th_echo.start()

    server = SocketServer.TCPServer(('127.0.0.1', 8002), AIServer)
    server.serve_forever()

    for i in range(0,4):
        ths[i].join()
