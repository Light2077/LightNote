from flask import Blueprint, render_template
blog_bp = Blueprint('blog', __name__)


# 测试用代码
@blog_bp.route('/')
def index():
    return render_template("blog/index.html")


@blog_bp.route('/category')
def show_category():
    return render_template("blog/category.html")


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/post')
def show_post():
    return render_template('blog/post.html')
