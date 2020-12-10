from flask import Flask, render_template, redirect, request, url_for, session, flash

from chat import chat
import random as rand


app = Flask(__name__)
app.register_blueprint(chat, url_prefix='/chat')





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





if __name__ == "__main__":
    app.run(debug=True)