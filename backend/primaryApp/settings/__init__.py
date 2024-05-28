import os
# 通过环境变量 ENV判断当前是生产环境还是开发环境

if os.environ.get('ENV') == 'production':
    # 生产环境
    print('生产环境')
    from .pro import *
else:
    # 开发环境
    print('开发环境')
    from .dev import *
