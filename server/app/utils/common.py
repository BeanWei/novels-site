from functools import wraps
from flask import abort, session, jsonify, g
from flask_login import current_user
from werkzeug.routing import BaseConverter
from .response_code import RET

# from app.models import Permission

class RegexConverter(BaseConverter):
    ''' U - N - U -S - E - D
    自定义静态文件路由转换器
    '''
    def __init__(self, map, *args):
        super(RegexConverter, self).__init__(map)
        self.regex=args[0]

def login_required(view_func):
    """登录校验装饰器
    :param func:函数名 
    :return: 闭包函数名
    """
    # 装饰器装饰一个函数时，会修改该函数的__name__属性
    # 如果希望装饰器装饰之后的函数，依然保留原始的名字和说明文档,就需要使用wraps装饰器，装饰内存函数
    @wraps(view_func)
    def wrapper(*args,**kwargs):
        #从session中或取user_id
        user_id=session.get('user_id')
        if not user_id:
            #用户未登录
            return jsonify(re_code=RET.SESSIONERR,msg='用户未登录')
        else:
            #用户已登录使用g变量保存住user_id，方便被装饰的函数中调用g变量获取user_id。
            g.user_id=user_id
            return view_func(*args,**kwargs)

    return wrapper

#TODO: 权限验证
# def permission_required(permission):
#     '''
#     权限验证装饰器
#     :param permission-> 指定权限
#     :return 装饰器
#     '''
#     def decorator(f):
#         @wraps(f)
#         def inner(*args, **kwargs):
#             if not current_user.power(permission):
#                 abort(403)
#             return f(*args, **kwargs)
#         return inner
#     return decorator

# def admin_required(view_func):
#     '''
#     管理员权限验证
#     :param view_func-> 视图方法
#     :return 装饰器
#     '''
#     return permission_required(Permission.ADMIN)(f)