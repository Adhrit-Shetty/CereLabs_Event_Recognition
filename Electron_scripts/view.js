var $ = require('jquery'); // jQuery now loaded and assigned to $
var ipAddress = 'http://localhost';
var port = 3000;
const io = require('socket.io-client');
var spawn = require("child_process").spawn;
var path = require('path');
// var isPortFree = require('is-port-free');
var valid = 0;
var ports = [3000, 4000, 5000, 8765, 8000, 9000];
var count = 0;
var sock_list =[];
var unused_port = require('get-unused-port-in-list')
var async = require('async');

function start_websocket(data) {
    var url = document.getElementById('path').value
    var flag = -1;
    console.log(url);
    unused_port(ports)
        .then((unusedPort) => {
            async.series([function (next) {
                console.log(unusedPort);
                console.log(__dirname);
                var python = spawn('python3', [path.join(__dirname, '..', 'Python_scripts/websock.py'), unusedPort.toString(), url], {
                    detached: true,
                    stdio: 'ignore'
                });
                python.unref();
                console.log(python);
                next();
            }], function (err) {
                if (err) {
                    console.log(err);
                    alert(err);
                } else {
                    x = valid
                    valid++;
                    console.log(x)
                    setTimeout(() => {
                        connect(unusedPort, x);
                    }, 2000);
                }
            })
        })
        .catch((error) => {
            console.log(error)
            console.log('all used')
            // All ports are busy 
        })
    // console.log(path.join(__dirname, '..', 'Python_scripts/test.py'))
}


function connect(port, value) {
    console.log(port+'---'+value+"---"+valid);
    var ws = new WebSocket("ws://localhost:"+port);
    var x = 0;
    var height;
    var width;
    if (value != (valid - 1)) {
        ws.close();
    }
    ws.onmessage = function (evt) {
        console.log(port+'---'+value+"---"+valid);
        if(value == (valid - 1)) {
            var received_msg = evt.data;
            var urlCreator = window.URL || window.webkitURL;
            console.log(urlCreator)
            console.log(received_msg)
            var imageUrl = urlCreator.createObjectURL(received_msg);
            document.querySelector("#img").src = imageUrl;
        }
        else{
            console.log('has to close'+port);
            ws.close();
            console.log('done!');
        }
    };
    ws.onclose = function () {
        // websocket is closed.
        console.log('Connection is closed:'+port)
    };

    // window.onbeforeunload = function(event) {
    //    socket.close();
    // };
}


function switch_con() {
    var url = document.getElementById('loadPy').value
    console.log('connecting to:' + url);
    x = valid;
    valid++;
    connect(url,x)
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