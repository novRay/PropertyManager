# coding: utf-8
from flask import Blueprint, render_template
from flask_login import current_user, login_required

from models import Notice

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
@login_required
def index():
    notice = Notice.query.order_by(Notice.created_at.desc()).first()
    return render_template('index.html', notice=notice, user=current_user)
