from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
ais_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('detection_req', namespace='/ai')
def detection_start(msg):
    print('Recv detection request, data url: ', str(msg))
    ais_client.send(msg['data'].encode('utf-8'))
    emit('detection_res', {'data': 'detection success'})

@socketio.on('connect', namespace='/ai')
def process_connect():
    print('Client connected')
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/ai')
def process_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    ais_client.connect(('127.0.0.1', 8002))
    socketio.run(app)
    