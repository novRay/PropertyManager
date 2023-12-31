# coding: utf-8
from exts import db
from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from models import Message, User

message_bp = Blueprint('message', __name__)


@message_bp.route('/messages')
@login_required
def view_messages():
    # 查询当前用户所有收到的消息并按ID降序排列
    received_messages = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.id.desc()).all()
    return render_template('message/view_messages.html', received_messages=received_messages, user=current_user)


@message_bp.route('/send_message', methods=['GET', 'POST'])
@login_required
def send_message():
    receiver_name = request.args.get('receiver_name', "")
    if request.method == 'POST':
        receiver_name = request.form.get('receiver_name')
        content = request.form.get('content')

        # 检查接收者是否存在
        receiver = User.query.filter_by(username=receiver_name).first()
        if not receiver:
            flash('目标用户名不存在！', 'error')
            return redirect(url_for('message.send_message'))

        # 普通用户只能给管理员发私信
        if not current_user.is_admin and not receiver.is_admin:
            flash('不能发送非管理员用户！', 'error')
            return redirect(url_for('message.send_message'))

        # 创建新的消息并提交数据库
        new_message = Message(sender_id=current_user.id, receiver_id=receiver.id, content=content)
        db.session.add(new_message)
        db.session.commit()
        flash('消息发送成功', 'success')
        return redirect(url_for('message.view_messages'))

    return render_template('message/send_message.html', receiver_name=receiver_name, user=current_user)
