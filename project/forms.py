from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField, TextAreaField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Optional, NoneOf, ValidationError, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
import email_validator





# registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Verify Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


# login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

#New Matrix Form
class NewMatrixForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    new_matrix = TextAreaField(validators=[DataRequired()])
    submit = SubmitField("Add Matrix")

#Calculate Matrix Form
class CalculateMatrixForm(FlaskForm):
    inpt = StringField(validators=[DataRequired()])
    submit = SubmitField("Calculate")

# Function Form
class FunctionForm(FlaskForm):
    range = IntegerField("Enter x range", validators=[DataRequired()])
    colors = [("k", "Black"), ("b", "Blue"), ("r", "Red"), ("g", "Green"), ("y", "Yellow")]
    color = RadioField("Type", choices=colors, validators=[DataRequired()])
    function = StringField("y= ", validators=[DataRequired()])
    submit = SubmitField("Enter")

# Profile Form
class SettingsForm(FlaskForm):
    profile_photo = FileField(validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'images only'), Optional()])
    bio = TextAreaField("Bio")
    gender = SelectField("Gender", choices=[('I would rather not say','I would rather not say'),('Male','Male'), ('Female','Female'), ('Other', 'Other')], validators=[Optional()])
    submit = SubmitField("Update Settings")

#Hangman input form
class HangmanForm(FlaskForm):
    letter = StringField("Enter a letter", validators=[DataRequired(),Length(max=1)])
    #su
#logout Form
class LogoutForm(FlaskForm):
    logout = SubmitField("Logout")

class DeleteForm(FlaskForm):
    delete = SubmitField("Delete Account")

def getImage(user):
  import base64

  try:
    image = base64.b64encode(user).decode('ascii')
  except:
      img = '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'

      image = img

  return image