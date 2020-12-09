from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import random as rand
from main import log
chat = Blueprint('chat', __name__, static_folder='static', template_folder='templates')


@chat.route('/create',methods = ["POST","GET"])
def createChat():
    if log():
        session['code'] = rand.randint(1000, 9999)

        db.session.add(rooms(code=session['code'], msg=session['user']+ " entered the chat.",members=1))
        db.session.commit()
        return redirect(url_for('room'))
    else:
        return redirect(url_for('home'))
@chat.route('/join',methods=["GET","POST"])
def joinChat():
    if log():
        if request.method == "GET":
            return render_template("join.html")
        else:
            session['code'] = request.form['code']

            myRoom = rooms.query.filter_by(code=session['code']).first()
            if myRoom is None:

                flash("room not found")
                return render_template("join.html")
            else:
                myRoom.members += 1
                myRoom.msg += ","+session['user']+ " entered the chat."
                db.session.commit()
                return redirect(url_for('room'))
    else:
        return "user ny sign"

@chat.route("/room", methods = ["GET","POST"])
def room():
    myRoom = rooms.query.filter_by(code=session['code']).first()
    if request.method == "POST":
        print(request.form)
        print(len(request.form))
        if len(request.form) == 0:
            myRoom.msg +=","+session['user']+ " left the chat."
            myRoom.members -= 1
            if myRoom.members == 0:
                db.session.delete(myRoom)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            myRoom.msg += ","+session['user']+":  "+request.form['chat']
            db.session.commit()


    msgs = myRoom.msg.split(',')

    for i in msgs:
        flash(i)

    return render_template('chat.html',code = session['code'],user=session['user'],members = myRoom.members)
@chat.route('/refresh', methods=['GET',"POST"])
def refresh():
    myRoom = rooms.query.filter_by(code=session['code']).first()
    msgs = myRoom.msg.split(',')

    for i in msgs:
        flash(i)
    return render_template('chat.html', code=session['code'], user=session['user'], members=myRoom.members)

@chat.route("/joinRandom")
def random():
    myRoom = rooms.query.first()
    myRoom.msg += "," + session['user'] + " entered the chat."
    myRoom.members += 1
    db.session.commit()
    return redirect(url_for('room'))