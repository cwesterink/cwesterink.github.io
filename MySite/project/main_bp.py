


from flask import Blueprint, render_template, session,request, flash
from flask_login import login_required, current_user

main_bp = Blueprint('main_bp', __name__, static_folder='static', template_folder='templates')

@main_bp.route('/', methods=['POST', "GET"])
def index():
    session['matrix'] = dict()
    if request.method == "GET" or request.method == 'POST':
        return render_template("index.html")










"""
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


"""

