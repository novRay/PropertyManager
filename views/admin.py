# coding: utf-8
from exts import db
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from models import User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/user_approval')
@login_required
def user_approval():
    if current_user.is_admin:  # 确保只有管理员可以访问这个页面
        unapproved_users = User.query.filter_by(approved=False).all()
        return render_template('admin/user_approval.html', unapproved_users=unapproved_users)
    else:
        flash('你没有权限访问这个页面', 'error')
        return redirect(url_for('user.profile'))

@admin_bp.route('/approve_user/<int:user_id>')
@login_required
def approve_user(user_id):
    if current_user.is_admin:  # 确保只有管理员可以批准用户
        user = User.query.get(user_id)
        if user:
            user.approved = True
            db.session.commit()
            flash(f'{user.username} 已批准', 'success')
        return redirect(url_for('admin.user_approval'))
    else:
        flash('你没有权限执行这个操作', 'error')
        return redirect(url_for('user.profile'))

