from flask import render_template, flash, url_for, redirect
from flask_blog import app
from flask_blog.forms import LoginForm, RegistrationForm


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
