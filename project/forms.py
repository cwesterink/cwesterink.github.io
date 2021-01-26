from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField, TextAreaField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Optional, NoneOf, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
import email_validator





# registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Verify Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


# login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# Function Form
class FunctionForm(FlaskForm):
    range = IntegerField("Enter x range", validators=[DataRequired()])
    colors = [("k", "Black"), ("b", "Blue"), ("r", "Red"), ("g", "Green"), ("y", "Yellow")]
    color = RadioField("Type", choices=colors, validators=[DataRequired()])
    function = StringField("y= ", validators=[DataRequired()])
    submit = SubmitField("Enter")

# Profile Form
class SettingsForm(FlaskForm):
    profile_photo = FileField(validators=[FileAllowed(['jpg', 'png'], 'images only'), Optional()])
    bio = TextAreaField("Bio")
    gender = SelectField("Gender", choices=[('I would rather not say','I would rather not say'),('Male','Male'), ('Female','Female'), ('Other', 'Other')], validators=[Optional()])
    privacy = BooleanField("Private")
    submit = SubmitField("Update Settings")

#logout Form
class LogoutForm(FlaskForm):
    logout = SubmitField("Logout")

def getImage(user):
  import base64

  try:
    image = base64.b64encode(user).decode('ascii')
  except:
    image = None
  return image