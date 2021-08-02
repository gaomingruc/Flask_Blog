from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from flask_wtf.recaptcha import validators
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField("用户名", validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("密码", validators=[DataRequired()])
    confirm_password = PasswordField(
        "密码确认", validators=[DataRequired(), EqualTo(fieldname="password")])
    submit = SubmitField("提交注册")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("用户名已存在，请换一个用户名")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("邮箱已存在，请换一个邮箱")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("密码", validators=[DataRequired()])
    remember = BooleanField("记住我")
    submit = SubmitField("登陆")


class UpdateAccountForm(FlaskForm):
    username = StringField("用户名", validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField("用户照片", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("提交修改")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("用户名已存在，请换一个用户名")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("邮箱已存在，请换一个邮箱")


class PostForm(FlaskForm):
    title = StringField("标题", validators=[DataRequired()])
    content = TextAreaField("内容", validators=[DataRequired()])
    submit = SubmitField("发送")
