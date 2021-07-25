from datetime import datetime
from enum import unique
from flask import Flask, render_template, url_for, flash, redirect
from sqlalchemy.orm import backref
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# CSRF表单保护
app.config["SECRET_KEY"] = "f79d917aebac39316c419e53d0721f70"
# sqlite数据库地址
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return "User(%s, %s, %s)" % (self.username, self.email, self.image_file)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return "Post(%s, %s)" % (self.title, self.date_posted)


@app.route('/base')
def base():
    """基模版"""
    return render_template("base.html")


@app.route('/')
@app.route('/index')
def index():
    """主页"""
    return render_template("index.html")


@app.route('/about')
def about():
    """关于"""
    return render_template("about.html", title="关于")


@app.route('/login', methods=["GET", "POST"])
def login():
    """登陆"""
    form = LoginForm()
    if form.validate_on_submit():
        flash("%s的账户登陆成功" % form.email.data, "success")
        return redirect(url_for("index"))
    return render_template("login.html", title="登陆", form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    """注册"""
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("%s的账户创建成功" % form.username.data, "success")
        return redirect(url_for("index"))
    return render_template("register.html", title="注册", form=form)
