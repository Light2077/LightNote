from flask import Flask
from flask_mail import Mail, Message
mail = Mail()
app = Flask(__name__)
app.config["MAIL_SERVER"] = "smtp.qq.com"
app.config["MAIL_USERNAME"] = "223@qq.com"
app.config["MAIL_PASSWORD"] = "xxx"
mail.init_app(app)
@app.route("/")
def index():
    msg = Message("Hello",
                  sender="223@qq.com",
                  recipients=["123@qq.com"])
    mail.send(msg)
    return "success!"