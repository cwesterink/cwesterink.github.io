from flask import Blueprint, render_template, session, redirect, request, url_for, session, flash, make_response, Response


import random
from flask import Blueprint, render_template, session, redirect, request, url_for, session, flash, make_response
from flask_socketio import send, emit, SocketIO, join_room, leave_room, rooms, close_room
from flask_login import current_user, login_required
game_bp = Blueprint('game_bp', __name__, static_folder='GameStatic', template_folder='templates')

from flask_socketio import SocketIO,send,emit,join_room,leave_room, namespace





@game_bp.route('/hangman')
def hangman():
    return render_template('hangman.html')




namespace = "/tictactoe"


rooms = dict()
players = dict()

from project import socketio


@game_bp.route('/tictactoe')
@login_required
def TicTacToe():

    return render_template('tictactoe.html', rooms = rooms)



@socketio.on('create',namespace=namespace)
def create(data):
    room = data['room']
    rooms[room] = {'isFull':False,'board':[["","",""],["","",""],["","",""]]}
    players[room] = [{'user':current_user.username,'ready':False}]
    join_room(room, namespace=namespace)
    print(rooms)
    user = current_user.username
    send(f"{user} has join {room}'s game.", room=room, namespace=namespace)
    emit('join', {'room': room,"user":current_user.username,'isFull':False}, room=room, namespace=namespace)
    emit('showRoom',{'room':room,'isFull':False}, namespace=namespace, broadcast=True)


@socketio.on('playCell',namespace=namespace)
def playCell(data):
    coords = data['coords']
    player = data['player']
    room = data['room']
    row,col = coords[0], coords[1]

    if rooms[room]['board'][row][col] == "":

        if players[room][0]['user'] == player:
            symbol = "X"
            turn = players[room][1]['user']
        else:
            symbol = "O"
            turn = players[room][0]['user']

        rooms[room]['board'][row][col] = symbol

        print(rooms[room]['board'])
        emit('placeSymbol',{'coords':coords,'symbol':symbol,'turn':turn}, room=room, namespace=namespace)

        isOver = checkWin(rooms[room]['board'])
        if isOver == True:
            emit('gameOver', {'msg': f"{player} has won the game"}, room=room, namespace=namespace)
        if isOver == 'tie':
            emit('gameOver', {'msg': f"Tie Game"}, room=room, namespace=namespace)


def checkWin(board):
    center = board[1][1]

    if center != "":
        #\
        if board[0][0] == center == board[2][2] != "":
            return True
        #/
        if board[2][0] == center == board[0][2] != "":
            return True
        #-
        if board[1][0] == center == board[1][2] != "":
            return True
        #|
        if board[0][1] == center == board[2][1] != "":
            return True

    if board[0][0] == board[0][1] == board[0][2] != "":
        return True

    if board[0][2] == board[1][2] == board[2][2] != "":
        return True

    if board[2][2] == board[2][1] == board[2][0] != "":
        return True

    if board[2][0] == board[1][0] == board[0][0] != "":
        return True

    for row in board:
        if "" in row:
            return False

    return 'tie'




@socketio.on('rNewGame', namespace=namespace)
def rNewGame(data):

    room = data['room']
    print(room,current_user.username)
    if room == current_user.username:
        players[room][0]['ready'] = True
    else:
        players[room][1]['ready'] = True


    if players[room][1]['ready'] and players[room][0]['ready']:
        players[room][0]['ready'] = False
        players[room][1]['ready'] = False
        rooms[room]['board'] = [["","",""],["","",""],["","",""]]
        emit('reset',{},room=room,namespace=namespace)

    else:
        emit('wait',{},room=request.sid, namespace=namespace)
        emit('requestPlay',{'player':current_user.username},room=room,include_self=False, namespace=namespace)












@socketio.on('join', namespace=namespace)
def join(data):
    user = current_user.username
    room = data['room']
    players[room] += [{'user':user,'ready':False}]
    rooms[room]['isFull'] = True
    print(f'{user} has joined {room}"s room')
    join_room(room,namespace=namespace)
    send(f"{user} has join {room}'s game.",room=room,namespace=namespace)
    emit("join", {'room':room,'user':current_user.username,'isFull':True,'turn':players[room][0]['user']}, room=room, namespace=namespace)
    emit('showRoom',{'room':room,'isFull':True}, namespace=namespace, broadcast=True)

@socketio.on('close', namespace=namespace)
def close(data):
    room = data['room']
    rooms.pop(room)
    players.pop(room)

    emit('leave',{'room':room,'reason':'close'},room=room ,namespace=namespace)
    close_room(room=room, namespace=namespace)
    emit('delRoom', {'room': room}, broadcast=True, namespace=namespace)

@socketio.on('leave',namespace=namespace)
def leave(data):
    usr = data['user']
    room = data['room']
    print("user left the room")
    rooms[room] = {'isFull':False,'board':[['','',''],['','',''],['','','']]}
    players[room].pop(1)
    print(players[room])

    emit('leave', {'room': room, 'reason': 'leave','who':usr}, room=room, namespace=namespace)
    leave_room(room, namespace=namespace)
    emit('showRoom', {'room': room, 'isFull': False}, namespace=namespace, broadcast=True)




