import os

from flask import Blueprint, render_template, jsonify, session, request

from aj.models import User, Area, House, db, Facility, HouseImage
from utils.functions import is_login

home_blue = Blueprint('home', __name__)


@home_blue.route('/source/', methods=['GET'])
def source():
    return render_template('myhouse.html')


@home_blue.route('/my_home/', methods=['GET'])
def my_home():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    username = user.name
    houses = House.query.all()
    my_houses = []
    other_houses = []
    if user.id_card:
        house_list = []
        for house in houses:
            house_images = HouseImage.query.filter_by(house_id=house.id).all()
            for image in house_images:
                house.images.append(image)
            house_list.append(house.to_full_dict())
        for my_house in house_list:
            if my_house['user_name'] == username:
                my_houses.append(my_house)
            else:
                other_houses.append(my_house)
        return jsonify({'code':200, 'msg':'请求成功', 'id_card': user.id_card,
                        'username': username,'my_house':my_houses,'other_house':other_houses})
    else:
        return jsonify({'code': 201, 'msg': '请求成功'})


@home_blue.route('/newhouse/', methods=['GET'])
def newhouse():
    return render_template('newhouse.html')


@home_blue.route('/my_newhouse/', methods=['GET'])
def my_newhouse():
    facilities = Facility.query.all()
    facilities_list = [facility.to_dict() for facility in facilities]
    areas = Area.query.all()
    data = []
    for area in areas:
        data.append(area.to_dict())
    return jsonify({'code':200, 'msg': '请求成功', 'areas':data, 'facilities':facilities_list})


@home_blue.route('/sub_newhouse/', methods=['GET'])
def sub_newhouse():

    title = request.args.get('title')
    price = request.args.get('price')
    area_id = request.args.get('area_id')
    address = request.args.get('address')
    room_count = request.args.get('room_count')
    acreage = request.args.get('acreage')
    unit = request.args.get('unit')
    capacity = request.args.get('capacity')
    beds = request.args.get('beds')
    deposit = request.args.get('deposit')
    min_days = request.args.get('min_days')
    max_days = request.args.get('max_days')
    facility = request.args.getlist('facility')
    if not title:
        return jsonify({'code': 1, 'msg': '房屋标题未填写'})
    if not price:
        return jsonify({'code': 2, 'msg': '每晚价格未填写'})
    if not area_id:
        return jsonify({'code': 3, 'msg': '未选择所在城区'})
    if not address:
        return jsonify({'code': 4, 'msg': '未填写详细地址'})
    if not room_count:
        return jsonify({'code': 5, 'msg': '未填写出租房间数量'})
    if not acreage:
        return jsonify({'code': 6, 'msg': '未填写房间面积'})
    if not unit:
        return jsonify({'code': 7, 'msg': '请输入房间描述'})
    if not capacity:
        return jsonify({'code': 8, 'msg': '请输入宜住人数'})
    if not beds:
        return jsonify({'code': 9, 'msg': '请输入卧床配置'})
    if not deposit:
        return jsonify({'code': 10, 'msg': '请输入押金金额'})
    if not min_days:
        return jsonify({'code': 11, 'msg': '请输入最小入住天数'})
    if not max_days:
        return jsonify({'code': 12, 'msg': '请输入最大入住天数'})
    if not facility:
        return jsonify({'code': 13, 'msg': '请选择房屋设施'})
    house = House()
    session_id = session.get('user_id')
    house.user_id = session_id
    house.title = title
    house.price = price
    house.address = address
    house.area_id = area_id
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days
    # house.facilities = facility
    for i in facility:
        home_facility = Facility.query.get(i)
        house.facilities.append(home_facility)

    db.session.add(house)
    db.session.commit()
    session['house_id'] = house.id
    return jsonify({'code': 200, 'msg': '请求成功'})


@home_blue.route('/patch_image/', methods=['PATCH'])
def patch_image():

    patch_image = request.files.get('house_image')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath((__file__))))
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    MEDIA_DIR = os.path.join(STATIC_DIR, 'media')
    path = os.path.join(MEDIA_DIR, patch_image.filename)
    patch_image.save(path)
    session_id = session.get('user_id')
    user = User.query.get(session_id)
    session_house = session.get('house_id')
    house = House.query.get(session_house)
    if not house.index_image_url:
        house.index_image_url = patch_image.filename
        house.add_update()
    house_image = HouseImage()
    house_image.house_id = house.id
    house_image.url = path
    house_image.add_update()
    return jsonify({'code': 200, 'msg': '请求成功', 'image': patch_image.filename})


@home_blue.route('/detail/<int:id>/', methods=['GET'])
def detail(id):
    return render_template('detail.html')


@home_blue.route('/my_detail/<int:id>/', methods=['GET'])
def my_datail(id):
    images = HouseImage.query.filter_by(house_id=id).all()
    house = House.query.get(id)
    user = User.query.filter_by(id=house.user_id).first()
    facilties_list = [facility.to_dict() for facility in house.facilities]
    image_list = [house.price]
    session_user_id = session['user_id']
    if user.id == session_user_id:
        pre_order = 1
    else:
        pre_order = 0
    for image in images:
        image_url = ''
        image_url += image.url.split('\\')[5:][-1]
        image_list.append(image_url)
    return jsonify({'code':200, 'msg': '请求成功', 'pre_order': pre_order,
                    'images': image_list,'user': user.to_basic_dict(),'facilities':facilties_list})