from flask import Blueprint, render_template
from bluelog.models import Post
blog_bp = Blueprint('blog', __name__)


# 测试用代码
@blog_bp.route('/test')
def test():
    from flask_login import current_user
    print(type(current_user), current_user)
    print("is_authenticated", current_user.is_authenticated)
    print("is_active", current_user.is_active)
    print("is_anonymous", current_user.is_anonymous)
    print("get_id()", current_user.get_id())
    return "test"


@blog_bp.route('/')
def index():
    posts = Post.query.limit(10).all()
    return render_template("blog/index.html", posts=posts)


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    return render_template("blog/category.html")


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    return render_template('blog/post.html')
