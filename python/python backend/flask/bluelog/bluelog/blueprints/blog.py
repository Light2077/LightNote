from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from flask_login import current_user
from bluelog.extensions import db
from bluelog.forms import AdminCommentForm, CommentForm
from bluelog.models import Post, Category, Comment
blog_bp = Blueprint('blog', __name__)


# 测试用代码
@blog_bp.route('/test_current_user')
def test_current_user():
    from flask_login import current_user
    print(type(current_user), current_user)
    print("is_authenticated", current_user.is_authenticated)
    print("is_active", current_user.is_active)
    print("is_anonymous", current_user.is_anonymous)
    print("get_id()", current_user.get_id())
    return "test"


@blog_bp.route('/')
def index():
    flash("hello", category="success")
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.order_by(
        Post.timestamp.desc()).paginate(page=page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/index.html', pagination=pagination, posts=posts)


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(
        Post.timestamp.desc()).paginate(page=page, per_page=per_page)
    posts = pagination.items

    return render_template("blog/category.html", category=category, pagination=pagination, posts=posts)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(
        Comment.timestamp.asc()).paginate(page=page, per_page=per_page)
    comments = pagination.items

    # 测试用
    from bluelog.forms import CommentForm, AdminCommentForm
    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['BLUELOG_EMAIL']
        form.site.data = url_for('.index')
    else:
        form = CommentForm()
    return render_template('blog/post.html', post=post, pagination=pagination, comments=comments, form=form)
