from flask import Blueprint, render_template, session, redirect, request, url_for, session, flash, make_response, Response
from flask_socketio import send, SocketIO
from flask_login import current_user, login_required
from .forms import getImage
from .models import History
from . import db
chat_bp = Blueprint('chat_bp', __name__, static_folder='static', template_folder='templates')




@chat_bp.route('/', methods=['POST', 'GET'])
@login_required
def chat():
	print('chat')
	hist = History.query.all()
	history = []
	for msg in hist:
		history += [msg.message]

	return render_template('chat.html', name = current_user.username,history = history)

from project import socketio

@socketio.on('connect')
def connect():
	print(f"{current_user.username} has connected")

@socketio.on('disconnect')
def disconnect():
	print(f"{current_user.username} has disconnected")

@socketio.on('message')
def handle(msg):
	import datetime
	tme = datetime.datetime.now()
	hour = str(tme.hour % 12)
	min = str(tme.minute)


	if int(min)<10:
		min = f"0{min}"

	if msg[:10] == "data:image":
		msg = f'<img src="{msg}" width="200" height="200" alt="Pic">'

	msg = current_user.username+": "+msg
	msgHist = msg
	pic = getImage(current_user.image)

	msg = f'<img src="data:;base64,{pic}" width="30" height="30" alt="Pic">'+msg
	msg = f'<p>{msg}<right>{hour}:{min}</right></p>'

	send(msg, broadcast=True)

	while len(History.query.all()) >= 30:
		firstMsg = History.query.first()
		db.session.delete(firstMsg)


	db.session.add(History(message=msgHist))
	db.session.commit()


