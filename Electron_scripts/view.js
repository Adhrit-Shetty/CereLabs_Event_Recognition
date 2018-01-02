var $ = require('jquery') // jQuery now loaded and assigned to $
var ipAddress = 'http://localhost'
var port = 3000
const io = require('socket.io-client');
var spawn = require("child_process").spawn;
var path = require('path')
// var isPortFree = require('is-port-free');
var ports = [3000, 4000, 5000, 8765, 8000, 9000]
var count = 0
var unused_port = require('get-unused-port-in-list')
var async = require('async')

function start_websocket(data) {
    var url = document.getElementById('path').value
    var flag = -1;
    console.log(url);
    unused_port(ports)
        .then((unusedPort) => {
            async.series([function(next){
                console.log(unusedPort); 
                console.log(__dirname);
                var python = spawn('python', [path.join(__dirname, '..', 'Python_scripts/websock.py'), unusedPort.toString(), url ]);
                console.log(python);
                python.stderr.on('data', function (buf) {
                    var textChunk = buf.toString('utf8');
                    console.log('buf=', textChunk);
                    next(textChunk);
                })
                next();
                // python.stdout.on('data', function (buf) {
                //     var textChunk = buf.toString('utf8')
                //     console.log('buf=', textChunk)
                // })                    
            }], function(err) {
                if(err){
                    console.log(err);
                }
                else{
                    setTimeout(() => {
                        connect(unusedPort);                        
                    }, 2000);
                }
            })
        })
        .catch(() => {
            console.log('all used')
            // All ports are busy 
        })
    // console.log(path.join(__dirname, '..', 'Python_scripts/test.py'))
}


function connect(port) {
    // const socket = io('http://localhost:3000');
    // console.log(socket)
    // var onevent = socket.onevent;
    // console.log(onevent)
    // socket.on("*",function(event,data) {
    //     console.log(event);
    //     console.log(data);
    // });
    var ws = new WebSocket("ws://localhost:"+port);
    var x = 0;
    var height;
    var width;
    ws.onmessage = function (evt) {
        var received_msg = evt.data;
        if (x == 0) {
            data = JSON.parse(received_msg)
            if (data.message) {
                console.log(data.message)
            } else {
                console.log(data)
                console.log(data.width);
                console.log(data.height);
                height = data.height;
                width = data.width;
                x++;
                console.log(x)
            }
        } else {
            console.log(received_msg)
            var urlCreator = window.URL || window.webkitURL;
            var imageUrl = urlCreator.createObjectURL(received_msg);
            document.querySelector("#img").src = imageUrl;
        }
    };
    ws.onclose = function () {
        // websocket is closed.
        alert("Connection is closed...");
    };

    // window.onbeforeunload = function(event) {
    //    socket.close();
    // };
}

function run_py() {
    console.log('here!');
    //Note that you need to activate the virtualenv before starting the electron app if you want the correct version of python to work 
    console.log(path.join(__dirname, '..', 'Python_scripts/test.py'))
    var python = spawn('python', [path.join(__dirname, '..', 'Python_scripts/test.py')]);
    console.log(python)
    python.stderr.on('data', function (buf) {
        console.log('buf=', buf)
    })
    python.stdout.on('data', function (buf) {
        var textChunk = buf.toString('utf8')
        console.log('buf=', textChunk)
    })
}