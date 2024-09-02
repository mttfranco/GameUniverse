from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blogcanada.models import User, Post
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(4, 20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submmit_button = SubmitField('Create Account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("E-mail already exist. Please try another e-mail.")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exist. Please try another username.")


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    still_conected = BooleanField('Keep me logged in')
    login_button = SubmitField('Login')


class FormEditProfile(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(4, 20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    profile_picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'jfif'])])
    button_wow = BooleanField('World of Warcraft')
    button_mu = BooleanField('Mu Online')
    button_shaiya = BooleanField('Shaiya Online')
    button_bda = BooleanField('Black Desert')
    button_cs = BooleanField('Counter Strike')
    button_starcraft = BooleanField('StarCraft')
    button_tibia = BooleanField('Tibia')
    confirm_button = SubmitField('Edit Profile')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("E-mail already exist. Please try another e-mail.")


class FormCreatePost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(2, 140)])
    post_body = TextAreaField('Body', validators=[DataRequired()])
    ok_button = SubmitField('Create Post')



