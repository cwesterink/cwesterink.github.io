from flask import Blueprint, render_template, session, redirect, request, url_for, session, flash, make_response, Response

from flask_login import current_user, login_required
import random
hangman_bp = Blueprint('hangman_bp', __name__, static_folder='static', template_folder='templates')

@hangman_bp.route("/", methods=["GET", "POST"])
def hangman():
    words = ["hello, boat"]
    if request.method == "POST":
        if True:
            pass




    if request.method == "GET":
        session['lives'] = 10
        session['word'] = random.choice(words)
        session['hidden'] = "_ "*len(session['word'])
        session['hidden'] =  session['hidden'][:-1]
        session['lettersChosen'] = []









    return render_template("hangman.html", hidden = session['hidden'], img = "img")


