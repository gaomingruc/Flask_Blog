from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# CSRF表单保护
app.config["SECRET_KEY"] = "f79d917aebac39316c419e53d0721f70"
# sqlite数据库地址
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

from flask_blog import routes
