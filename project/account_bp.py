# Flask imports
import base64
from io import BytesIO

from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, send_file
from flask_login import login_user, logout_user, login_required, current_user
# Database imports
from werkzeug.datastructures import CombinedMultiDict

from .models import User
from . import db
from .forms import getImage

# form imports

from .forms import RegistrationForm, LoginForm, SettingsForm, LogoutForm, DeleteForm
from urllib.parse import urlparse, urljoin


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


account_bp = Blueprint('account_bp', __name__, static_folder='static', template_folder='templates')


# registration route
@account_bp.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        flash("you are already logged in")
        return redirect(url_for('main_bp.index'))

    def validate_user(user):
        for letter in user:
            if letter in e:
                return False
        return True

    form = RegistrationForm()
    e = "/!@#$%^&*():,.:?'}{|-+= "
    if request.method == "POST":

        if form.validate_on_submit():
            if validate_user(form.username.data):
                if User.query.count() == 0:
                    user = User(username=form.username.data,status='admin')
                else:
                    user = User(username=form.username.data)


                user.set_password(form.password.data)
                db.session.add(user)

                try:
                    db.session.commit()
                except:
                    error = "Error: Email and/or username already exists. Would you like to login?"
                    return render_template('register.html', title='Register', form=form, error=error)
                else:
                    return redirect(url_for("account_bp.login"))
            else:
                error = "Invalid Character(s) For Username"
                return render_template('register.html', title='Register', form=form, error=error)

        else:
            error = "Error passwords do not match."
            return render_template('register.html', title='Register', form=form, error=error)
    else:  # Request is a GET or frontend error
        return render_template('register.html', title='Register', form=form)


@account_bp.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash("you are already logged in")
        return redirect(url_for('main_bp.index'))
    if request.method == "POST":

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:  # if User exists
                if user.check_password(form.password.data):  # if password matches

                    login_user(user, remember=form.remember.data)

                    next_page = request.args.get('next')
                    if not is_safe_url(next_page):
                        return abort(400)

                    return redirect(next_page or url_for('account_bp.profile', username=current_user.username))

                else:  # password was incorrect
                    error = 'Incorrect Password. Try again.'
            else:  # User does not exist
                error = 'User not recognized'

        else:  # non  valid email
            error = 'Please enter existing user.'
        return render_template('login.html', form=form, error=error)

    return render_template('login.html', form=form)





@account_bp.route('/user/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return "user does not exist"

    return render_template("profile.html", user=user)


@account_bp.route('/settings', methods=['POST', "GET"])
@login_required
def settings():
    settingsForm = SettingsForm(bio=current_user.bio,gender=current_user.gender)
    deleteForm = DeleteForm()
    logoutForm = LogoutForm()
    if request.method == "POST":

        if settingsForm.validate_on_submit():
            if settingsForm.profile_photo.data:
                current_user.image = settingsForm.profile_photo.data.read()

            if settingsForm.bio.data:
                bio = settingsForm.bio.data
                current_user.bio = bio
            if settingsForm.gender.data:
                gender = settingsForm.gender.data
                current_user.gender = gender


            db.session.commit()
            return redirect(url_for('account_bp.profile', username=current_user.username))

    return render_template('settings.html', settingsForm=settingsForm, logoutForm=logoutForm, deleteForm = deleteForm)

@account_bp.route('/delete')
@login_required
def delete():
    d = current_user.username
    logout_user()
    delt = User.query.filter_by(username=d).first()
    db.session.delete(delt)
    db.session.commit()
    return render_template('index.html')

@account_bp.route('/logout', methods=['POST', "GET"])
@login_required
def logout():
    logout_user()
    flash("logged out")
    return redirect(url_for('main_bp.index'))

@account_bp.route('/user')
@login_required
def users():
    users = User.query.all()
    return render_template("users.html", users=users)




