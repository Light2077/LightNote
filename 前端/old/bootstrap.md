https://bootstrap-flask.readthedocs.io/en/latest/

https://flask-bootstrap-zh.readthedocs.io/zh/latest/index.html

flask-bootstrap 与 bootstrap-flask的区别

https://zhuanlan.zhihu.com/p/39799223

https://getbootstrap.com/docs/3.4/

在`exts/__init__.py`

```python
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap()
```

在`apps/__init__.py`

```python
def create_app():
    ...
    bootstrap.init_app(app)
    ...
    return app

```

