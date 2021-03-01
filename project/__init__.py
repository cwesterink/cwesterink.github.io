import os

from flask import Flask, flash, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user,login_user, logout_user, login_required
from flask_socketio import SocketIO

from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()





def create_app():
    global socketio
    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins='*')

    app.config['SECRET_KEY'] = 'const'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['WTF_CSRF_SECRET_KEY'] = 'a random string'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_message = "You must Login to view this page"

    login_manager.login_view = 'account_bp.login'

    #login_manager.anonymous_user = None
    login_manager.init_app(app)

    from .models import User
    @login_manager.unauthorized_handler
    def unauthorized():
        flash(login_manager.login_message)
        return redirect(url_for('account_bp.login'))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprint Setup
    from .account_bp import account_bp
    app.register_blueprint(account_bp)

    from .math_bp import math_bp
    app.register_blueprint(math_bp, url_prefix='/math')

    from .main_bp import main_bp
    app.register_blueprint(main_bp)

    from .chat_bp import chat_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')



    return app



app = create_app()




#Below are global variables for jinja2
app.jinja_env.globals['user'] = current_user
from .forms import getImage
app.jinja_env.globals['getImage'] = getImage

if __name__ == 'project.__init__':
    socketio.run(app, port=int(os.environ.get('PORT', '5000')))






