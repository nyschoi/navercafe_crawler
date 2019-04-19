from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from cafe_kakao.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
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

    def validate_kakaoid(self, kakaoid):
        user = User.query.filter_by(kakaoid=kakaoid.data).first()
        if user:
            raise ValidationError(
                '이미 가입한 카카오ID임. 오타가 아닌지?')


class LoginForm(FlaskForm):
    kakaoid = StringField('카카오id',
                          validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    kakaoid = StringField('카카오id',
                          validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_kakaoid(self, kakaoid):
        if kakaoid.data != current_user.kakaoid:
            user = User.query.filter_by(kakaoid=kakaoid.data).first()
            if user:
                raise ValidationError(
                    '이미 가입한 카카오ID임. 오타가 아닌지?')


class PostForm(FlaskForm):
    clubid = StringField('네이버 카페 ID', validators=[DataRequired()])
    menuid = StringField('카페 게시판 ID', validators=[DataRequired()])
    description = TextAreaField('설명. 알아듣기 쉽게 쓰자', validators=[DataRequired()])
    submit = SubmitField('Post')
