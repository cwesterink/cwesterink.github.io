let socket;
let room;
let turn;
let user;
let isFull;
let gameActive = true;
let canvas = document.getElementById('game');
let ctx = canvas.getContext('2d');
let width = canvas.getAttribute('width');
let height= canvas.getAttribute('height');
let txt = document.getElementById('winTxt')
let cell={
    width: canvas.getAttribute('width')/3,
    height: canvas.getAttribute('height')/3
}

function displayTurn(){
    let msg;
    if (turn==user){
        msg = "your";
    }else{
        msg = turn+"'s";
    }
    document.getElementById('whoturn').innerText = "It is "+msg+" turn";
}

function getMousePosition(event) {
    let rect = canvas.getBoundingClientRect();
    var x = event.pageX - rect.left;
    var y = event.pageY - rect.top;

    var col = Math.trunc(x / (canvas.getAttribute('width') / 3));

    var row = Math.trunc(y / (canvas.getAttribute('height') / 3));

    return [row,col];

        }

canvas.addEventListener('mousedown',function (e) {

        if(user==turn && gameActive==true){

            var coord = getMousePosition(e);
            socket.emit('playCell',{'coords':coord,'player':user, 'room':room});

            }
        else {
            alert('not your turn')
        }






});

function draw() {
    ctx.beginPath();
    ctx.moveTo(width/3, 0);
    ctx.lineTo(width/3, height);



    ctx.moveTo(2*width/3, 0);
    ctx.lineTo(2*width/3, height);

    ctx.moveTo(0, height/3);
    ctx.lineTo(width,height/3);

    ctx.moveTo(0, 2*height/3);
    ctx.lineTo(width,2*height/3);
    ctx.closePath();
    ctx.stroke();

}

function clear(){

    var w = ctx.canvas.width;
    var h = ctx.canvas.height;

ctx.clearRect(0, 0, w, h);
}

function displayX(row,col){
    ctx.beginPath();

    //tl to br
    ctx.moveTo(col*(width/3)+cell.width/4,row*(height/3)+cell.height/4);
    ctx.lineTo(col*(width/3)+cell.width*3/4,row*(height/3)+cell.height*3/4);

    //tr to bl
    ctx.moveTo(col*(width/3)+cell.width*3/4,row*(height/3)+cell.height/4);
    ctx.lineTo(col*(width/3)+cell.width/4,row*(height/3)+cell.height*3/4);

    ctx.closePath();
    ctx.stroke();

}

function displayO(row,col){
    ctx.beginPath()

    ctx.moveTo(col*(width/3)+cell.width/2,row*(height/3)+cell.height/2);

    ctx.beginPath();
    ctx.arc(col*(width/3)+cell.width/2, row*(height/3)+cell.height/2, cell.height/3, 0, 2 * Math.PI, false);

    ctx.closePath()

    ctx.stroke();
}

function createRoom(){

    room = document.getElementById('user').innerHTML;
    socket.emit('create',{'room':room});
}

function closeRoom(){
    socket.emit('close',{'room':room})
}

function leaveRoom(){
    socket.emit('leave',{'room':room,'user':user});
}

function joinRoom(nRoom){
    if (room !== undefined){
            alert("You are already in room");
        }
    else{

        socket.emit('join', {'room':nRoom});

    }
}

function playAgain(){
    var area = document.getElementById('reset-area');
    var btn = document.getElementById('cancel');

    btn.hidden=false;
    document.getElementById('reset').hidden = true

    socket.emit('rNewGame', {'user':user,'room':room})



}

window.onbeforeunload = function () {
        leaveRoom()
    }


$(document).ready(function() {

    socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + "/tictactoe");
    user = document.getElementById('user').innerHTML;
    socket.on('reset', function (data){

        gameActive=true;
        document.getElementById('winTxt').innerHTML = "";
        document.getElementById('reset-area').hidden = true;
        document.getElementById('cancel').hidden = true
        turn = room;

        clear()
        draw()
        displayTurn()



    })

    socket.on('requestPlay', function (data){
        txt.innerHTML+= "<br>"+ data['player'] +"has requested to play again"
    })
    socket.on('wait', function (data){
        txt.innerHTML +=  "<br>"+"waiting for other player"
    })



    socket.on('delRoom', function (data){
        var nRoom = data['room']
        document.getElementById(nRoom).remove();

    })

    socket.on('showRoom', function (data){
        var nRoom = data['room']
        isFull = data['isFull']
        let p;

        if (document.getElementById(nRoom)==null){
            p = document.createElement('li');
        }
        else{
            p = document.getElementById(nRoom);
        }

        p.setAttribute('id',nRoom)

        if (isFull) {
            p.innerHTML =  nRoom + "'s room     (Full)"
        }
        else if(room !== undefined){
            p.innerHTML =  nRoom + "'s room"
        }
        else{
            p.innerHTML = nRoom + "'s room" + "<button onclick='joinRoom(this.parentNode.id)'>Join</button>"
        }

        var lst = document.getElementById('roomList');

        lst.appendChild(p);



    })

    socket.on('gameOver', function (data){
        var msg = data['msg']
        gameActive=false;

        var area = document.getElementById('reset-area');
        var txt = document.getElementById('winTxt');
        var btn = document.getElementById('reset');
        btn.hidden = false
        area.hidden = false

        txt.innerText = msg

        document.getElementById('whoturn').innerText = ""




    })

    socket.on("placeSymbol", function (data){
        var symbol = data['symbol'];
        let coords = data['coords'];

        if (symbol=="O"){
            displayO(coords[0],coords[1]);
        }
        else if(symbol=="X"){
            displayX(coords[0],coords[1]);
        }
        turn = data['turn']
        displayTurn()
    })

    socket.on("join", function (data){
        document.getElementById('msg').innerHTML = ""

        room = data['room']
        if (user == room){
            document.getElementById('cRoomBtn').hidden = false
        }
        else{
            document.getElementById('lRoomBtn').hidden = false
        }
        document.getElementById('nRoomBtn').setAttribute('hidden','true');
        var isFull = data['isFull'];
        var b = document.getElementById('msg');
        if(isFull){
            document.getElementById('game').hidden = false
            draw()
            b.innerHTML+= "Room is Full Let the games Begin<br>";
            turn = data['turn'];
            displayTurn()




        }
        else{
            b.innerHTML+="Waiting for one more player...<br>"
        }
    })

    socket.on('message', function (data){

        var msg = data

        var b = document.getElementById('msg');
        b.innerHTML+= msg+"<br>";
    })


    socket.on('leave', function (data){
        document.getElementById('game').hidden = true
        clear()

        document.getElementById('whoturn').innerText = ""
        if(data['reason'] == 'close'){

            document.getElementById('msg').innerHTML = "The Host has Closed the room"
            room = undefined;
            document.getElementById('cRoomBtn').hidden = true
            document.getElementById('lRoomBtn').hidden = true
            document.getElementById('nRoomBtn').hidden = false
        }
        else{

            document.getElementById('msg').innerHTML = data['who']+' has left the room'

            if(user==data['who']){

                room = undefined;
                document.getElementById('cRoomBtn').hidden = true
                document.getElementById('lRoomBtn').hidden = true
                document.getElementById('nRoomBtn').hidden = false
            }
            else{
                document.getElementById('msg').innerHTML += "Waiting for new player to arrive"

            }


        }

    })

});