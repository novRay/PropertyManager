# coding: utf-8

from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate

import config
from models import User
from views.admin import admin_bp
from views.auth import auth_bp
from views.message import message_bp
from views.user import user_bp
from views.post import post_bp
from exts import db

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
migrate = Migrate(app, db)

# 建表
with app.app_context():
    db.create_all()
    # create_admin_user()


# 登录模块初始化
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"  # 设置登录视图的端点

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


# 注册所有blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(post_bp)
app.register_blueprint(message_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run()
