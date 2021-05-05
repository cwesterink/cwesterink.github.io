from flask import Blueprint, render_template, session, redirect, request, url_for, session, flash, make_response
from flask_socketio import send, emit, SocketIO, join_room, leave_room, rooms, close_room
from flask_login import current_user, login_required
from .forms import getImage
from . import db

from .models import User
chat_bp = Blueprint('chat_bp', __name__, static_folder='static', template_folder='templates')


@chat_bp.route('/', methods=['POST', 'GET'])
@login_required
def chat():
    rooms = ['Global', 'Quick Chat', 'Dray', 'Admins']
    return render_template('chatroom.html', rooms=rooms)



from project import socketio

namespace = "/chat"
clients = dict()

@socketio.on('test', namespace=namespace)
def leave(data):
    print("\n\n\n\ndvdsefefs\n\n\n ")



@socketio.on('join', namespace=namespace)
def join(data):
    room = data['room']
    join_room(room, namespace=namespace)
    msg = 'joined the chat'
    chat(msg, room, namespace)

    user = current_user


    if room not in clients:
        clients[room] = dict()

    print(user.username+" has joined the room")
    print(clients)
    data = {'user': user.username, 'src': f'data:;base64,{getImage(user.image)}'}
    emit('addIcon', data, broadcast=True, namespace=namespace, room=room)


    for client in list(clients[room].keys()):
        usr = User.query.filter_by(username=client).first()
        print(client)
        data = {'user': usr.username, 'src': f'data:;base64,{getImage(usr.image)}'}
        emit('addIcon', data, broadcast=True, namespace=namespace, room=request.sid)

    clients[room][user.username] = request.sid




@socketio.on('leave', namespace=namespace)
def leave(data):
    room = data['room']
    clients[room].pop(current_user.username)
    leave_room(room, namespace=namespace)

    if len(clients[room]) == 0:
        print('close room')
        print(rooms(namespace=namespace))
        clients.pop(room)
        close_room(room=room,namespace=namespace)
    else:
        msg = 'left the chat'
        chat(msg, room, namespace)
        emit('delIcon', current_user.username, broadcast=True, namespace=namespace, room=room)



@socketio.on('message', namespace=namespace)
def handle(data):
    print(rooms())
    import datetime
    msg = data['msg']
    room = data['room']
    from time import strftime, localtime
    tme = strftime('%I:%M', localtime())

    chat(msg, room, namespace)


def chat(msg, room, namespace, toSelf=True):
    msg = current_user.username + ": " + msg

    pic = getImage(current_user.image)

    msg = f'<img src="data:;base64,{pic}" width="30" height="30" alt="Pic" class="w3-circle">' + msg
    msg = f'<p>{msg}</p>'
    #msg = f'<p>{msg}<right>{tme}</right></p>'
    send(msg, broadcast=True, namespace=namespace, room=room,include_self=toSelf)
