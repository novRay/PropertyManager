# coding: utf-8
from werkzeug.security import generate_password_hash

from exts import db
from models import User


def create_admin_user():
    # 创建一个管理员用户
    admin_user = User(
        username='admin',
        password=generate_password_hash('123456'),
        is_admin=True,
        approved=True,
        email='admin@pm.com',
    )

    # 添加到数据库并提交
    db.session.add(admin_user)
    db.session.commit()