from flask import Flask, render_template, url_for, request
from flask_wtf import FlaskForm
# from wtforms import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.secret_key = 'abc123'
app.port = 5002
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

@app.route('/test_form')
def test_form():
	form = LoginForm()
	return render_template('test_form.html', form=form)


@app.route('/test_referrer')
def test_referrer():
    return (
        f"request.referrer: {request.referrer}<br>"
        f"request.host_url: {request.host_url}<br>"
        f"request.path: {request.path}<br>"
        f"request.full_path: {request.full_path}<br>"
        f"request.host: {request.host}<br>"
        f"request.url: {request.url}<br>"
    )


@app.route('/')
def index():
    url = url_for('test_referrer')
    return f"<a href='{url}'>test referrer</a>"

if __name__ == '__main__':
   app.run(port=5002)