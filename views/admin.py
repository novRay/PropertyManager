# coding: utf-8
from exts import db
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from models import User, Notice

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/user_approval')
@login_required
def user_approval():
    # 检查当前用户是否管理员
    if not current_user.is_admin:
        flash('你没有权限访问这个页面', 'error')
        return redirect(url_for('post.view_posts'))
    # 查询未批准的用户并按ID降序排列
    unapproved_users = User.query.filter_by(approved=False).order_by(User.id.desc()).all()
    return render_template('admin/user_approval.html', unapproved_users=unapproved_users, user=current_user)

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
        return redirect(url_for('post.view_posts'))

@admin_bp.route('/notice', methods=['GET', 'POST'])
@login_required
def publish_notice():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        new_post = Notice(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index.index'))
    return render_template('admin/publish_notice.html', user=current_user)

