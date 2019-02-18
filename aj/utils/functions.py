from functools import wraps

from flask import session, redirect, url_for


# def is_login(func):
#     @wraps(func)
#     def check_is_login(*args, **kwargs):
#         try:
#             session['user_id']
#             return func(*args, **kwargs)
#         except Exception as e:
#             return redirect(url_for('user.login'))
#     return check_is_login


# 登录装饰器
def is_login(func):
    @wraps(func)
    def check_is_login(*args, **kwargs):
        if 'user_id' in session:
            # 判断session中是否存在登录的标识user_id
            return func(*args, **kwargs)
        else:
            # 如果没有登录则跳转到登录页面
            return redirect(url_for('user.login'))
    return check_is_login
