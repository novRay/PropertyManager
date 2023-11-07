# coding: utf-8
import pytz
from flask_login import UserMixin
from datetime import datetime

from config import TIME_ZONE
from exts import db


class User(db.Model, UserMixin):
    __table_name__ = "User"
    id = db.Column(db.Integer, primary_key=True)  # 用户ID（主键）
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名
    password = db.Column(db.String(200), nullable=False)  # 密码
    approved = db.Column(db.Boolean, default=False, nullable=False)  # 是否已批准
    is_admin = db.Column(db.Boolean, default=False, nullable=False)  # 是否是管理员

    email = db.Column(db.String(120), unique=True, nullable=True)  # 邮箱
    full_name = db.Column(db.String(100), nullable=True)  # 真实姓名
    sex = db.Column(db.String(100), nullable=True)  # 性别
    address = db.Column(db.String(200), nullable=True)  # 住址


class Post(db.Model):
    __table_name__ = "Post"
    id = db.Column(db.Integer, primary_key=True)  # 帖子ID（主键）
    title = db.Column(db.String(100), nullable=False)  # 帖子标题
    content = db.Column(db.Text, nullable=False)  # 帖子内容
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 发帖用户ID（外键）
    user = db.relationship('User', backref='posts')  # 帖子与用户的关联关系
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone(TIME_ZONE)))  # 创建时间


class Comment(db.Model):
    __table_name__ = "Comment"
    id = db.Column(db.Integer, primary_key=True)  # 评论ID（主键）
    content = db.Column(db.Text, nullable=False)  # 评论内容
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 评论用户ID（外键）
    user = db.relationship('User', backref='comments')  # 评论与用户的关联关系
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # 评论所属帖子ID（外键）
    post = db.relationship('Post', backref='comments')  # 评论与帖子的关联关系
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone(TIME_ZONE)))  # 评论创建时间


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 消息ID（主键）
    content = db.Column(db.Text, nullable=False)  # 消息内容
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 发送者用户ID（外键）
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')  # 消息发送者与用户的关联关系
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 接收者用户ID（外键）
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')  # 消息接收者与用户的关联关系
    sent_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone(TIME_ZONE)))  # 消息发送时间


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 公告ID（主键）
    title = db.Column(db.String(100), nullable=False)  # 公告标题
    content = db.Column(db.Text, nullable=False)  # 公告内容
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone(TIME_ZONE)))  # 公告创建时间
