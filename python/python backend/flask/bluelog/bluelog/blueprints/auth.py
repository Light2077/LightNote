from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from bluelog.models import Admin

auth_bp = Blueprint('auth', __name__)

from bluelog.forms import LoginForm
@auth_bp.route('/test_login', methods=['GET', 'POST'])
def test_login():
    form = LoginForm()
    if request.method == "POST":
        print(form.username.data)
        print(form.password.data)
        print(form.remember.data)
        return "POST request"
    return render_template('auth/test_login.html', form=form)

    
@auth_bp.route('/test_request_method', methods=['GET', 'POST'])
def test_request_method():
    if request.method == "GET":
        print("GET request")
        return "GET return data"
    
    if request.method == "POST":
        print("POST request")
        return "POST return data"


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                return redirect(url_for('blog.index'))
        else:
            return "No account."
    
    return render_template("auth/login.html")


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return "注销成功"
