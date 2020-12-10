from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from calculator import simplify
#from chat import chat
import random as rand


app = Flask(__name__)

#app.register_blueprint(chat, url_prefix='/chat')



app.secret_key = "const"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQlALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class rooms(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    msg = db.Column(db.String)
    members = db.Column(db.Integer)
    def __init__(self, code, msg, members):
        self.code = code
        self.msg = msg
        self.members = members
def log():
    if 'user' in session:
        return True
    return False
@app.route('/', methods =["POST","GET"])
def home():
    if request.method =="GET" or request.method =='POST':
        if log():
            flash(f"Welsome {session['user']},you are logged in ")
        else:
            flash('you are not logged in')
        return render_template("home.html",login=log())
    
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

        db.session.add(rooms(code=session['code'], msg=session['user']+ " entered the chat.",members=1))
        db.session.commit()
        return redirect(url_for('room', code = session['code']))
    else:
        return redirect(url_for('home'))
@app.route('/join',methods=["GET","POST"])
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
                return redirect(url_for('room', code = session['code']))
    else:
        return render_template(url_for('home'))

@app.route("/room/<code>", methods = ["GET","POST"])
def room(code):
    try:
        myRoom = rooms.query.filter_by(code=session['code']).first()
    except:

        return redirect(url_for('home'))
    else:

    
        if len(request.form) != 0:
            myRoom.msg += ","+session['user']+":  "+request.form['chat']
            db.session.commit()

        msgs = myRoom.msg.split(',')
        for i in msgs:
            flash(i)
        return render_template('chat.html', code=session['code'], user=session['user'], members=myRoom.members)


@app.route('/leave', methods = ['GET','POST'])
def leave():
    myRoom = rooms.query.filter_by(code=session['code']).first()
    myRoom.msg +=","+session['user']+ " left the chat."
    myRoom.members -= 1
    if myRoom.members == 0:
        db.session.delete(myRoom)
    db.session.commit()

    return redirect(url_for('home'))


@app.route("/joinRandom")
def random():
    myRoom = rooms.query.first()
    print(myRoom.code)
    myRoom.msg += "," + session['user'] + " entered the chat."
    myRoom.members += 1
    db.session.commit()
    return redirect(url_for('room'))



@app.route('/calculator', methods = ['POST','GET'])
def clac():
    if request.method == 'GET':
        return render_template('calculator.html')

    else:
        session['calcInpt'] = request.form['input']
        num = simplify(session['calcInpt'])
        flash(session['calcInpt'])
        flash(num)
        return render_template('calculator.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)