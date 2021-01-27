from flask import Blueprint, render_template, session, redirect, request, url_for, session, flash, make_response, Response
from flask_socketio import send, SocketIO
from flask_login import current_user, login_required
from .forms import getImage
chat_bp = Blueprint('chat_bp', __name__, static_folder='static', template_folder='templates')



@chat_bp.route('/', methods=['POST', 'GET'])
@login_required
def chat():
	return render_template('chat.html', name = current_user.username)

from project import socketio

@socketio.on('connect')
def connect():
	print(f"{current_user.username} has connected")

@socketio.on('disconnect')
def disconnect():
	print(f"{current_user.username} has disconnected")

@socketio.on('message')
def handle(msg):
	msg = current_user.username+": "+msg
	print("message "+msg)
	pic = getImage(current_user.image)
	msg = f'<img src="data:;base64,{pic}" width="30" height="30" alt="Pic">'+msg

	send(msg, broadcast=True)


