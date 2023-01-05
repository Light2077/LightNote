from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from bluelog.models import Admin

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return "已登录！"
    admin = Admin.query.first()
    login_user(admin, remember=True)
    return "登录成功"


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return "注销成功"
