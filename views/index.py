# coding: utf-8
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from models import Notice

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
@login_required
def index():
    # 查询最新的三条通知
    notices = Notice.query.order_by(Notice.created_at.desc()).limit(3).all()
    return render_template('index.html', notices=notices, user=current_user)
