from flask import Flask, render_template
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

@app.route('/')
def index():
	form = LoginForm()
	return render_template('index.html', form=form)