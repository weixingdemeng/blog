import os
import random
import re

from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required

from aj.models import Area, User, db, HouseImage, House, Order
from utils.functions import is_login

user_blue = Blueprint('user',__name__)

# 前端
@user_blue.route('/register/',methods=['GET'])
def register():
    return render_template('register.html')

# 后端
@user_blue.route('/register/',methods=['POST'])
def my_register():
    # 获取参数
    # errors = {}
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')
    # 1.验证参数是否都填写了
    # if not mobile:
    #     errors['mobile_error'] = '你还没有输入手机号'
    if not all([mobile, imagecode, passwd, passwd2]):
        return jsonify({'code': 1001, 'msg': '请填写完整参数'})
    # 2.验证手机号是否正确
    if not re.match('^1[3456789]\d{9}$', mobile):
        return jsonify({'code': 1002, 'msg': '手机号不正确'})
    # 3.验证图片验证码
    if  session['image_code'] != imagecode:
        return jsonify({'code': 1003, 'msg': '输入的验证码不正确'})
    # 4.密码和确认密码是否一致
    if passwd != passwd2:
        return jsonify({'code': 1004, 'msg':'密码不一致'})
    # 5.验证手机号是否被注册
    user = User.query.filter(User.phone==mobile).first()
    if  user:
        return jsonify({'code': 1005, 'msg': '手机号已经被注册，请重新注册'})

    # 6.创建注册信息
    user = User()
    user.phone = mobile
    user.password = passwd
    user.name = mobile
    user.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})

@user_blue.route('/code/',methods=['GET'])
def get_code():
    # 获取验证码
    # 方式1：后端生成图片，并返回验证码图片的地址(不推荐)
    # 方式2：后端只生成一个随机参数，返回给前端，在页面中再生成图片
    s = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''
    for i in range(4):
        code += random.choice(s)
    session['image_code'] = code
    return jsonify({'code':200 , 'msg':'请求成功', 'data': code})


@user_blue.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@user_blue.route('/my_login/', methods=['GET'])
def my_login():
    # 实现登录
    mobile = request.args.get('mobile')
    password = request.args.get('password')
    # 校验参数是否完整
    # 获取手机号对应的用户信息
    # 校验密码是否正确
    # 登录标识设置
    if not all([mobile, password]):
        return jsonify({'code': 2001, 'msg': '请输入手机号和密码'})
    user = User.query.filter(User.phone==mobile).first()
    if not user:
        return jsonify({'code': 2002, 'msg': '你输入手机号还未注册'})
    if not user.check_pwd(password):
        return jsonify({'code': 2003, 'msg': '你输入的密码不正确'})
    session['user_id'] = user.id
    return jsonify({'code':200, 'msg':'成功'})


@user_blue.route('/my/', methods=['GET'])
@is_login
def my():
    return render_template('my.html')


@user_blue.route('/user_info/',methods=['GET'])
@is_login
def user_info():
    # 获取用户信息
    user_id = session['user_id']
    user = User.query.get(user_id)
    return jsonify({'code': 200, 'msg': '请求成功', 'data': user.to_basic_dict()})


@user_blue.route('/logout/', methods=['GET'])
def logout():
    del session['user_id']
    return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/auth/',methods=['GET'])
def auth():
    return render_template('auth.html')


@user_blue.route('/auth2/', methods=['GET'])
def auth2():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if user.id_card:
        return jsonify({'code':200, 'msg':'请求成功', 'username': user.name, 'id_card':user.id_card})
    return jsonify({'code':201, 'msg': '请求成功'})


@user_blue.route('/my_auth/', methods=['GET'])
def my_auth():
    username = request.args.get('real_name')
    id_card = request.args.get('id_card')

    idcardReg = '^[1-9]\d{7}((0\d)|(1[0 - 2]))(([0|1|2]\d)|3[0-1])\d{3}$' \
                '|^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$'
    user = User.query.filter(User.name==username).first()
    # session_id_card = session.get['id_card']
    # session_user = User.query.filter(User.id == session.get['user_id'])
    # print(type(session_user ))
    if not all([username, id_card]):
        return jsonify({'code': 100, 'msg': '请输入真实姓名和身份证号'})
    if not user:
        return jsonify({'code': 102, 'msg': '你输入的用户没有登录'})
    if user.id_card:
        return jsonify({'code': 101, 'msg': '你输入的用户已经实名认证过了'})

    if not re.match(idcardReg, id_card):
        return jsonify({'code': 103, 'msg': '你输入的身份证号格式不正确'})
    user.id_card = id_card
    session['id_card'] = id_card
    db.session.add(user)
    db.session.commit()
    return jsonify({'code': 200, 'msg': ''})


@user_blue.route('/profile/', methods=['GET'])
def profile():
    return render_template('profile.html')


@user_blue.route('/my_profile/', methods=['PATCH'])
def my_profile():
    image = request.files.get('avatar')

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath((__file__))))
    # 获取媒体文件的路径
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    MEDIA_DIR = os.path.join(STATIC_DIR, 'media')
    path = os.path.join(MEDIA_DIR, image.filename)
    image.save(path)
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'code':3001, 'msg':'没有登录'})
    user.avatar = image.filename
    db.session.add(user)
    db.session.commit()
    #
    # update_user.name = user_name
    # update_user.phone = user_name
    # update_user.avatar = image.filename
    # db.session.add(update_user)
    # db.session.commit()
    return jsonify({'code':200, 'msg': '请求成功', 'path': image.filename})


@user_blue.route('/name_profile/', methods=['PATCH'])
def name_profile():
    user_name = request.form.get('name')
    session_user = session.get('user_id')
    user = User.query.filter(User.name == user_name).first()
    if user:
        return jsonify({'code':3001, 'msg': '你输入的用户名已经存在,请重新设置'})

    update_user = User.query.filter(User.id==session_user).first()
    update_user.name = user_name
    db.session.add(update_user)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@user_blue.route('/my_index/', methods=['GET', 'POST'])
def my_index():
    if request.method == 'GET':
        a = Area.query.all()
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            username = user.name
        else:
            username = ''
        areas = []
        images = HouseImage.query.all()
        image_list = list(set([image.url.split('\\')[-1] for image in images]))
        for area in a:
            area_obj = area.to_dict()
            areas.append(area_obj)
        areas.append(session.get('mobile'))
        return jsonify({'code': 200, 'areas': areas, 'username': username, 'image_list': image_list})
    if request.method == 'POST':
        id = request.form.get('aid')
        name = request.form.get('aname')
        start_time = datetime.strptime(request.form.get('sd'), '%Y-%m-%d')
        end_time = datetime.strptime(request.form.get('ed'), '%Y-%m-%d')
        all_houses = House.query.filter(House.area_id==id).all()
        # order_houses = []
        houses = []
        for house in all_houses:
            order_houses = Order.query.filter(Order.house_id==house.id).all()
            if order_houses:
                for order_house in order_houses:
                    if end_time<order_house.begin_date or start_time>order_house.end_date:
                        houses.append(order_house)
            else:
                houses.append(house)
        return_houses = [return_house.to_dict() for return_house in houses]
        return jsonify({'code':200, 'msg': '请求成功', 'houses': return_houses})

@user_blue.route('/logout/', methods=['POST'])
@is_login
def my_logout():
    del session['user_id']
    return jsonify({'code':200, 'msg': '请求成功'})


@user_blue.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


# @user_blue.route('/my_search/', methods=['GET'])
# def my_search():
#     # data_list = request.args.get('data_list')
#
#     return jsonify({'code': 200, 'msg': '请求成功'})


#
# @user_blue.route('/')
# def hello():
#     return 'hello flask'
#
#
# @user_blue.route('/load_index/',methods=['GET'])
# def load_index():
#     if request.method == 'GET':
#         return render_template('index.html')
#
#
# @user_blue.route('/index/',methods=['GET','POST'])
# def index():
#     if request.method == 'GET':
#         a = Area.query.all()
#         areas=[]
#         for area in a:
#             area_obj = area.to_dict()
#             areas.append(area_obj)
#         return jsonify({'code':200, 'areas':areas})
#
#
#
# @user_blue.route('/register/', methods=['GET','POST'])
# def register():
#     if request.method == 'GET':
#         return render_template('register.html')

