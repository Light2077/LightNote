import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
    TEST_CONFIG = 'test config'  # 用于测试

# 开发环境的配置


class DevelopmentConfig(BaseConfig):
    pass
# 测试环境的配置


class TestingConfig(BaseConfig):
    pass
# 生产环境的配置


class ProductionConfig(BaseConfig):
    pass


# 选择使用哪种配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
