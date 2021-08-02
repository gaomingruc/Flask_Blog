import os
import secrets
from PIL import Image
from flask import render_template, flash, url_for, redirect, request, abort
import flask_login
from flask_login.utils import login_required
from flask_blog import app, db, bcrypt
from flask_blog.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm
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
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


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


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("新博客发布了", "success")
        return redirect(url_for("index"))
    return render_template("create_post.html", title="New Post", form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("您的博客已修改", "success")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("update_post.html", title="Update Post", form=form, post=post)


@app.route("/post/<int:post_id>/delete")
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("您的博客已删除", "success")
    return redirect(url_for("index"))