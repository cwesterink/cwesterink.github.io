from flask import Blueprint, render_template, session, redirect, request, url_for, session, flash, make_response, Response

from flask_login import current_user, login_required
import random
game_bp = Blueprint('game_bp', __name__, static_folder='GameStatic', template_folder='templates')

from flask_socketio import SocketIO,send,emit,join_room,leave_room, namespace



#from project import socketio
@game_bp.route("/hangman")
def hangman():
    return render_template("hangman.html")


