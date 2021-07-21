from flask import Flask, render_template, url_for
app = Flask(__name__)


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
    return render_template("about.html")


@app.route('/login')
def login():
    """登陆"""
    return render_template("login.html")


@app.route('/register')
def register():
    """注册"""
    return render_template("register.html")
