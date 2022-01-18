### 接收json，返回json

```python
@app.route('/test_post', methods=['POST'])
def test_post():
    data = json.loads(request.get_data())
    data['id'] = 9527
    return jsonify(data)
```

测试

```python
data = {
    'name': 'lily',
    'age': 19
}
resp = requests.post("http://127.0.0.1:5000/test_post", json=data)
print(resp.json())
```

```
{'age': 19, 'id': 9527, 'name': 'lily'}
```


