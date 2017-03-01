from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField

class RegisterForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')
    captcha = RecaptchaField()