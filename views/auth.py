# coding: utf-8
from exts import db
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            if not user.approved:
                flash('账号尚未通过审核，请耐心等待', 'error')
            else:
                login_user(user)
                flash('登录成功', 'success')
                return redirect(url_for('user.profile'))  # Redirect to user profile page
        else:
            flash('登录失败，请检查用户名和密码', 'error')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('注销成功', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        address = request.form.get('address')

        if password1 != password2:
            flash('密码不一致，请重新输入', 'error')
        else:
            user = User.query.filter_by(username=username).first()
            if user:
                flash('用户名已被注册', 'error')
            else:
                new_user = User(username=username,
                                password=generate_password_hash(password1),
                                approved=False,
                                is_admin=False,
                                email=email,
                                full_name=full_name,
                                address=address,
                                )
                db.session.add(new_user)
                db.session.commit()
                flash('注册成功，请等待管理员审核', 'success')
                return redirect(url_for('auth.login'))
    return render_template('auth/register.html')
