from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
import email_validator




# registration form
class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[InputRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Verify Password', validators=[DataRequired(), EqualTo('password')])
  profile_photo = FileField(validators=[FileAllowed(['jpg', 'png'], 'images only')])
  submit = SubmitField('Register')


# login form
class LoginForm(FlaskForm):
  email = StringField('Email',
                      validators=[DataRequired(), Email()])
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
  profile_photo = FileField(validators=[FileAllowed(['jpg', 'png'], 'images only')])
  submit = SubmitField("Update Settings")

#logut Form
class Logout(FlaskForm):
  logout = SubmitField("Logout")