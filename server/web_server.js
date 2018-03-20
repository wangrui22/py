const express = require('express');
const net = require('net');

let app = express();
let http = require('http').Server(app);
let io = require('socket.io')(http);
http.listen(8081);

let socketMaps = {}

//client to AI server
let client = net.createConnection({host:"127.0.0.1", port:8005}, function() {
    console.log('tcp connect success.');
});

client.on('data', function(data){
    console.log('data stream >>>>');
    let data_str = data.toString();
    console.log('data: ', data_str);
    let datas = data_str.split('|');
    let users = datas[0].split(',');
    let data_url = datas[1];
    console.log('users: ', users);
    console.log('data_url: ', data_url)

    for(let key in socketMaps) {
        for(let i=0; i<users.length; ++i) {
            if (key == users[i]) {
                socketMaps[key].emit('detection_res', {code:1, data:data_url});
            }
        }
    }
});

client.on('end', function(data){
    console.log('close connection.');
    //接受到server的结果，并反馈给web前端
});

//websocket server to Web
io.on('connection', function(socket){
    console.log('a user connected');

    socket.on('login', data=>{
        socketMaps[data.user] = socket;
        socket.user = data.user;
        console.log(`user ${data.user} login.`);
    });

    socket.on('detection_req', data=>{
        console.log(`data is: ${data.data}`);
        const data_url = data.data;
        const msg = socket.user + '|' + data_url;
        console.log(`msg to ai server: ${msg}`);
        client.write(msg);
    });

    socket.on('disconnect', function(){
        const user = socket.user;
        delete socketMaps[user];
        console.log(`user ${user} disconnected.`);
    });
});

