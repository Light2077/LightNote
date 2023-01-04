import random
import time

from flask import Flask, render_template, Response
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('2.点击按钮通过服务端增加进度.html')


@app.route('/progress')
def progress():
    x = 0
    def generate(x):
        while True:
            # x = random.randint(10, 90)
            x = min(100, x + 3)
            if x >= 70:
                break
            time.sleep(0.2)
            yield f"data:{x}\n\n"
    return Response(generate(x), mimetype='text/event-stream')