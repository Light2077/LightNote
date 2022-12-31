import random
from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello!'


@app.route('/gold')
def get_gold():
    gold = random.randint(1, 100)
    return jsonify({'gold': gold})


# 解决跨域问题
@app.after_request
def func_res(resp):     
    res = make_response(resp)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res