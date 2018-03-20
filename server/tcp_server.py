import SocketServer

class EchoRequestServer(SocketServer.BaseRequestHandler):
    def handle(self):
        print('TCP server start...')
        conn = self.request
        print('get connection:', self.client_address)
        while True:
            client_data = conn.recv(1024)
            if not client_data:
                print('close connection')
                break
            print(client_data.decode('utf-8'))
            print('begin to send')
            conn.sendall(client_data)
        
if __name__ == '__main__':
    server = SocketServer.TCPServer(('127.0.0.1', 8000), EchoRequestServer)
    server.serve_forever()
