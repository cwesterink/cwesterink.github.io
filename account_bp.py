from flask import Blueprint, render_template, request, session, flash

# form instalations
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

account_bp = Blueprint('account_bp', __name__, static_folder='static', template_folder='templates')
account_bp.secret_key = "const"