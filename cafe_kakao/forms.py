from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from cafe_kakao.models import User


class RegistrationForm(FlaskForm):
    username = StringField('이름', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email(나중에 ID로 쓰일)',
                        validators=[DataRequired(), Email()])
    kakaoid = StringField('카카오ID',
                          validators=[DataRequired(), Length(min=2, max=20)])
    access_token = StringField('access_token',
                               validators=[DataRequired(), Length(max=100)])
    refresh_token = StringField('refresh_token',
                                validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('가입하기')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('이미 가입된 email')

    def validate_kakaoid(self, kakaoid):
        user = User.query.filter_by(kakaoid=kakaoid.data).first()
        if user:
            raise ValidationError('이미 가입된 카카오 계정')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('이미 사용중인 이메일')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    clubid = StringField('네이버 카페 ID', validators=[DataRequired()])
    menuid = StringField('카페 게시판 ID', validators=[DataRequired()])
    description = TextAreaField('설명(알아듣기 쉽게 쓰자)', validators=[DataRequired()])
    submit = SubmitField('Post')
