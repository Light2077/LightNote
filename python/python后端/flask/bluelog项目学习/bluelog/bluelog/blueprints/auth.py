from flask import Blueprint
auth_bp = Blueprint('auth', __name__)


# 测试用代码
@auth_bp.route('/')
def index():
    return "<h1>auth_bp</h1>"
