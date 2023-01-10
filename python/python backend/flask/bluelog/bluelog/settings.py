import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    TEST_CONFIG = 'test config'  # 用于测试
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')
    BLUELOG_EMAIL = "YourEmail@email.com"
    BLUELOG_POST_PER_PAGE = 10  # 每页多少篇文章
    BLUELOG_COMMENT_PER_PAGE = 5  # 每页显示多少评论


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


# 选择使用哪种配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
