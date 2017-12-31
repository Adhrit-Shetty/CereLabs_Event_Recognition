let $ = require('jquery')  // jQuery now loaded and assigned to $
let ipAddress = 'http://localhost'
let port = 3000
const io = require('socket.io-client');
// let socket = io();
// socket.connect('http://' + ipAddress + ':' + port);
let count = 0
document.getElementById('click-counter').innerHTML = count.toString()
document.getElementById('click-counter1').innerHTML = count.toString()
function update_count() {
    count++;
    document.getElementById('click-counter').innerHTML = count.toString()
    document.getElementById('click-counter1').innerHTML = count.toString()
    console.log('here!');
}

function connect(){
    // const socket = io('http://localhost:3000');
    // console.log(socket)
    // var onevent = socket.onevent;
    // console.log(onevent)
    // socket.on("*",function(event,data) {
    //     console.log(event);
    //     console.log(data);
    // });
    var ws = new WebSocket("ws://localhost:8765");
    var x = 0;
    var height;
    var width;
    ws.onmessage = function (evt) 
    {
        var received_msg = evt.data;
        if(x == 0){
            data = JSON.parse(received_msg)
            console.log(data)
            console.log(data.width);
            console.log(data.height);
            height = data.height;
            width = data.width;
            x++;
            console.log(x)
        } 
        else{
            console.log(received_msg)
            var urlCreator = window.URL || window.webkitURL;
            var imageUrl = urlCreator.createObjectURL(received_msg);
            document.querySelector("#img").src = imageUrl;
        }
    };
     
    ws.onclose = function()
    { 
       // websocket is closed.
       alert("Connection is closed..."); 
    };
         
    // window.onbeforeunload = function(event) {
    //    socket.close();
    // };
}