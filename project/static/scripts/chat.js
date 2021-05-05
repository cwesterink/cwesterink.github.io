let socket;
let room;





function selectRoom(newroom){
    if (room === undefined){

        room = newroom;
        socket.emit('join', {'room': room});


        // add room title
        var title = document.getElementById('roomLabel');
        title.innerHTML = room;


    }
    else if (room == newroom){
        alert('you are already in room')
    }
    else{


        socket.emit('leave', {'room': room});

        room = newroom;
        reset(room)


        socket.emit('join', {'room': room});
    }
}

function reset(room){
     // change to no room selected
    var title = document.getElementById('roomLabel');
    title.innerHTML = room;

    // erase icons
    var icons = document.getElementById('active-users');
    icons.innerHTML = '';

    // erase chat log
    var myList = document.getElementById('messages');
    myList.innerHTML = '';
}


window.onbeforeunload = function () {
    if (room!==undefined){
        socket.emit('leave', {'room': room});
        room=undefined;
    }

}
function exitChat(){


    socket.emit('leave', {'room': room});
    room=undefined;


    // delete home button
    var btn = document.getElementById('leftbtn');
    btn.parentNode.removeChild(btn)

    // add exit room button
    var a = document.createElement("a");
    a.setAttribute("id", "leftbtn");
    a.setAttribute('href','/')
    var txt = document.createTextNode("Home");
    a.appendChild(txt);
    var element = document.getElementById("nav");
    element.appendChild(a);

    reset('No room selected')
}

$(document).ready(function() {
    socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + "/chat");

    document.getElementById("inp").addEventListener("change", readFile);

    function readFile() {

            if (this.files && this.files[0]) {

                var FR = new FileReader();
                FR.addEventListener("load", function (e) {

                    var img = e.target.result.toString();
                    img = '<img src="'+img+'"width="200" height="200" alt="Pic">'
                    socket.send(img);
                });
                FR.readAsDataURL(this.files[0]);
            }
        }

    socket.on('delIcon',function (user){
        var icon = document.getElementById(user);
        icon.remove()

    });

    socket.on('addIcon',function(data){
                // add user image
                var username = data['user'];
                var src = data['src'];

                // user div
                var div = document.createElement('p')
                div.setAttribute('id',username)


                //image for icon
                var img = document.createElement("img");
                img.setAttribute('src',src)
                img.setAttribute('class','w3-circle')
                img.setAttribute('height','30')
                img.setAttribute('width','30')

                var text = document.createTextNode(username);
                div.appendChild(text);

                div.appendChild(img);



                //div.innerHTML = p.innerHTML + img
                var element = document.getElementById("active-users");
                element.appendChild(div);


            });



    socket.on('message', function (msg) {
                $("#messages").append('<li>' + msg + '</li>');
                chatWindow = document.getElementById('chat-window');
                var xH = chatWindow.scrollHeight;
                chatWindow.scrollTo(0, xH);
            });




    $('#sendImage').on('click', function (){
                var link = $('#image_link').val()
                if (link != ""){
                    $('#image_link').val('')
                    var msg = '<img src="'+link+'">'

                    socket.send({'msg':msg,'room':room});
                }

            })

    $('#sendbutton').on('click', function () {

                var msg = $('#myMessage').val();
                if (msg !== ''){
                    $('#myMessage').val('');

                    var loop = document.getElementById("loop");
                    var caps = document.getElementById("caps");

                    if (loop!=null){
                        if (caps.checked){
                        msg = msg.toUpperCase()
                        caps.checked = false;
                        document.getElementById("myMessage").autofocus;

                        };
                        if (loop.checked){
                            msg = "<marquee>"+msg+"</marquee>"
                            loop.checked = false;
                            document.getElementById("myMessage").autofocus;
                        };
                    }


                    socket.send({'msg':msg,'room':room});


                }


            });


    $('#myMessage').on("keypress", function (e) {
                var key = e.which;
                if (key == 13) {
                    document.querySelector('#sendbutton').click();

                }

            });

    });

