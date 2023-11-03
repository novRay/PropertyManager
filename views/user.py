# coding: utf-8
from exts import db
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html', user=current_user)


@user_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        new_email = request.form.get('email', current_user.email)
        new_full_name = request.form.get('full_name', current_user.full_name)
        new_sex = request.form.get('sex', current_user.sex)
        new_address = request.form.get('address', current_user.address)

        current_user.email = new_email
        current_user.full_name = new_full_name
        current_user.sex = new_sex
        current_user.address = new_address

        db.session.commit()
        # flash('个人信息已更新', 'success')
        return redirect(url_for('user.profile'))
    return render_template('user/edit_profile.html', user=current_user)
