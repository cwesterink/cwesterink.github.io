import os
from flask import Flask, flash, redirect, url_for, render_template, request
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user,login_user, logout_user, login_required
from flask_socketio import SocketIO
from flask_admin import Admin, BaseView , AdminIndexView


from flask_admin.contrib.sqla import ModelView
db = SQLAlchemy()


from .models import  User, Role
from . import db




def create_app():
    global socketio
    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins='*')



    app.config['SECRET_KEY'] = 'const'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://meqsgqxvktfdlt:d1ec5a68cb26e38a07fc59906616df44cce3bd9a54434162808e1b45a139bbf2@ec2-54-164-241-193.compute-1.amazonaws.com:5432/dblqtd0taenc53'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_SECRET_KEY'] = 'a random string'
    db.init_app(app)
    if False:
        db.create_all(app=app)
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
        usr = User.query.get(int(user_id))
        return usr

    # Blueprint Setup
    from .account_bp import account_bp
    app.register_blueprint(account_bp)

    from .math_bp import math_bp
    app.register_blueprint(math_bp, url_prefix='/math')

    from .main_bp import main_bp
    app.register_blueprint(main_bp)

    from .chat_bp import chat_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')

    from .game_bp import game_bp
    app.register_blueprint(game_bp)

    return app



app = create_app()




from flask_migrate import Migrate
migrate = Migrate(app, db)
m = True
if m:
    pass




@app.before_request
def before_request():
    if app.env == "development":
        return
    if request.is_secure:
        return

    url = request.url.replace("http://", "https://", 1)
    code = 301
    return redirect(url, code=code)






# ADD ADMIN FEATURES
from .adminViews import UserView, MyIndexView, MainView, RoleView
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3',index_view=MyIndexView())
admin.add_view(UserView(User, db.session))
admin.add_view(RoleView(Role,db.session))
admin.add_link(MenuLink(name='Home Page', url='/'))

#Below are global variables for jinja2
app.jinja_env.globals['user'] = current_user
from .forms import getImage
app.jinja_env.globals['getImage'] = getImage



if __name__ == 'project.__init__':

    socketio.run(app, port=int(os.environ.get('PORT', '5000')))
