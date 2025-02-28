
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class SignupForm(FlaskForm):
  fullName = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=40)])
  username = StringField("Username", validators=[DataRequired(), Length(min=2, max=40)])
  email = EmailField("Email", validators=[DataRequired(), Email()])
  password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
  confirmPassword = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
  submit = SubmitField("Sign Up")
  
class SignupForm(FlaskForm):
  email = EmailField("Email", validators=[DataRequired(), Email()])
  password = PasswordField("Password", validators=[DataRequired()])
  remember = BooleanField("Remember Me")
  submit = SubmitField("Log In")
  


