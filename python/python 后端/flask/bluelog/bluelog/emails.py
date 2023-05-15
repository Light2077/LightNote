from threading import Thread

from flask import url_for, current_app
from flask_mail import Message

from bluelog.extensions import mail


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subject, to, html):
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def send_new_comment_email(post):
    """ 当有新的读者评论时，发送邮件给管理员 """
    post_url = url_for('blog.show_post', post_id=post.id,
                       _external=True) + '#comments'
    send_mail(
        subject='New comment', to=current_app.config['BLUELOG_EMAIL'],
        html=f'<p>New comment in post <i>{post.title}</i>, click the link below to check:</p>'
        f'<p><a href="{post_url}">{post_url}</a></P>'
        f'<p><small style="color: #868e96">Do not reply this email.</small></p>'
    )


def send_new_reply_email(comment):
    """ 当评论被他人回复时，发邮件给被评论人 """
    post_url = url_for('blog.show_post', post_id=comment.post_id,
                       _external=True) + '#comments'
    send_mail(
        subject='New reply', to=comment.email,
        html=f'<p>New reply for the comment you left in post <i>{comment.post.title}</i>'
        f', click the link below to check: </p><p><a href="{post_url}">{post_url}</a></p>'
        '<p><small style="color: #868e96">Do not reply this email.</small></p>'
    )
