from flask import Blueprint
admin_bp = Blueprint('admin', __name__)


# 测试用代码
@admin_bp.route('/')
def index():
    return "<h1>admin_bp</h1>"
