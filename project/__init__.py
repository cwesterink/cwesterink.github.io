from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user,login_user, logout_user, login_required

from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()





def create_app():

    app = Flask(__name__)


    x = 2
    app.config['SECRET_KEY'] = 'const'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['WTF_CSRF_SECRET_KEY'] = 'a random string'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'account_bp.login'
    #login_manager.anonymous_user = None
    login_manager.init_app(app)

    from .models import User

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

    return app

app = create_app()




app.jinja_env.globals['user'] = current_user
from .forms import getImage
app.jinja_env.globals['getImage'] = getImage
