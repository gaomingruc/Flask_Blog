import os
import secrets
from PIL import Image
from flask import render_template, flash, url_for, redirect, request
import flask_login
from flask_login.utils import login_required
from flask_blog import app, db, bcrypt
from flask_blog.forms import LoginForm, RegistrationForm, UpdateAccountForm
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


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
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("%s的账户登陆成功" % form.email.data, "success")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("登陆失败，请检查用户名和密码", "warning")
    return render_template("login.html", title="登陆", form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    """注册"""
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("%s的账户创建成功，请登陆" % form.username.data, "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="注册", form=form)


@app.route("/logout")
def logout():
    """登出"""
    logout_user()
    return redirect(url_for("index"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """账户"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        user.username = form.username.data
        user.email = form.email.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        db.session.commit()
        flash("您的用户信息已更新", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/%s" % current_user.image_file)
    return render_template("account.html", title="账户", image_file=image_file, form=form)

