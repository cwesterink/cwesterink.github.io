from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

#from chat import chat
import random as rand


app = Flask(__name__)

#app.register_blueprint(chat, url_prefix='/chat')

db = SQLAlchemy(app)

app.secret_key = "const"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQlALCHEMY_TRACK_MODIFICATIONS'] = False



class chatRooms(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    msg = db.Column(db.String)
    members = db.Column(db.Integer)
    def __init__(self, code, msg, members):
        self.code = code
        self.msg = msg
        self.members = member




def log():
    if 'user' in session:
        return True
    return False

@app.route('/', methods =["POST","GET"])
def home():
    if request.method =="GET":

        if log():


            flash(f"Welsome {session['user']},you are logged in ")
        else:

            flash('you are not logged in')
        return render_template("home.html",login=log())
    else:
        session.clear()
        return redirect(url_for('home'))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":

        if log():
            return redirect(url_for('home'))
        else:
            flash('login to continue')
            return render_template("login.html")
    if request.method == "POST":
        session['user'] = request.form['name']
        return redirect(url_for('home'))
@app.route('/create',methods = ["POST","GET"])
def createChat():
    if log():
        session['code'] = rand.randint(1000, 9999)

        db.session.add(chatRooms(code=session['code'], msg=session['user']+ " entered the chat.",members=1))
        db.session.commit()
        return redirect(url_for('room'))
    else:
        return redirect(url_for('home'))

@app.route('/join',methods=["GET","POST"])
def joinChat():
    if log():
        if request.method == "GET":
            return render_template("join.html")
        else:
            session['code'] = request.form['code']

            myRoom = chatRooms.query.filter_by(code=session['code']).first()
            if myRoom is None:

                flash("room not found")
                return render_template("join.html")
            else:
                myRoom.members += 1
                myRoom.msg += ","+session['user']+ " entered the chat."
                db.session.commit()
                return redirect(url_for('room'))
    else:
        return redirect(url_for('home'))

@app.route("/room/<code>", methods = ["GET","POST"])
def room(num):
    myRoom = chatRooms.query.filter_by(code=num).first()
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
    return "Refresh"
    return render_template('chat.html',code = code,user=session['user'],members = myRoom.members)


@app.route("/joinRandom")
def random():
    myRoom = chatRooms.query.first()
    myRoom.msg += "," + session['user'] + " entered the chat."
    myRoom.members += 1
    db.session.commit()
    return redirect(url_for('room'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)