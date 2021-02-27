from flask import Blueprint, render_template, session, request, flash
from flask_login import login_required, current_user

main_bp = Blueprint('main_bp', __name__, static_folder='static', template_folder='templates')


@main_bp.route('/', methods=['POST', "GET"])
def index():
    #
    if request.method == "GET" or request.method == 'POST':
        return render_template("index.html")
