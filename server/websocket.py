# import simplejson
# import socket
# import sys
# import base64
# import hashlib
# import time

# HOST = '127.0.0.1'
# PORT = 9000
# MAGIC_STRING = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
# HANDSHAKE_STRING = "HTTP/1.1 101 Switching Protocols\r\n" \
#     "Upgrade:WebSocket\r\n" \
#     "Connection: Upgrade\r\n" \
#     "Sec-WebSocket-Accept: {1}\r\n" \
#     "WebSocket-Location: ws://{2}/chat\r\n" \
#     "WebSocket-Protocol:chat\r\n\r\n"

# def parse_data(msg):
#     v = ord(msg[1]) & 0x7f
#     if v == 0x7e:
#         p = 4
#     elif v == 0x7f:
#         p = 10
#     else:
#         p = 2

#     mask = msg[p:p+4]
#     data = msg[p+4:]

#     return ''.join([chr(ord(v) ^ ord(mask[k%4])) for k, v in enumerate(data)])

# def start():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     try:
#         sock.bind((HOST, PORT))
#         sock.listen(100)
#     except Exception as e:
#         print('bind error')
#         print(e)
#         sys.exit()

#     while True:
#         conn, add = sock.accept()

#         try:
#             handshake(conn)
#         finally:
#             print('finally')
#             conn.close()

#     sock.close()
#     pass

# def handshake(conn):
#     headers = {}
#     shake = conn.recv(1024)

#     print shake

#     if not len(shake):
#         print('len error')
#         return False

#     header, data = shake.split('\r\n\r\n', 1)
#     for line in header.split('\r\n')[1:]:
#         key, value = line.split(': ', 1)
#         headers[key] = value

#     if 'Sec-WebSocket-Key' not in headers:
#         print('this is not websocket, client close.')
#         print headers
#         conn.close()

#         return False

#     sec_key = headers['Sec-WebSocket-Key']
#     res_key = base64.b64encode(hashlib.sha1(sec_key + MAGIC_STRING).digest())

#     str_handshke = HANDSHAKE_STRING.replace('{1}', res_key).replace('{2}', HOST + ":" + str(PORT))
#     print str_handshke

#     conn.send(str_handshke)
#     time.sleep(1)
#     conn.send('%c%c%s' % (0x81, 6, 'suren1'))
#     msg = conn.recv(1024)
#     msg = parse_data(msg)
#     print('msg : ' + msg)

#     time.sleep(1)
#     conn.send('%c%c%s' % (0x81, 6, 'suren2'))
#     msg = conn.recv(1024)
#     msg = parse_data(msg)
#     print('msg : ' + msg)

#     time.sleep(1)
#     conn.send('%c%c%s' % (0x81, 6, 'suren3'))
#     msg = conn.recv(1024)
#     msg = parse_data(msg)
#     print('msg : ' + msg)

#     return True

#     pass

# if __name__ == '__main__':
#     try:
#         start()
#     except Exception as e:
#         print(e)



from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('test.html')
    #return '<h1>hello world!</h>'

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message2(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connected')
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)