from datetime import datetime

from flask import Blueprint, render_template, jsonify, session, request

from aj.models import House, Order
from utils.functions import is_login

order_blue = Blueprint('order',__name__)


@order_blue.route('/lorders/<int:id>/', methods=['GET'])
def lorders(id):
    return render_template('lorders.html')





@order_blue.route('/booking/<int:id>/', methods=['GET'])
@is_login
def booking(id):
    return render_template('booking.html')


@order_blue.route('/my_booking/<int:id>/', methods=['GET', 'POST'])
@is_login
def my_booking(id):
    if request.method == 'GET':
        house = House.query.get(id)
        return jsonify({'code': 200, 'msg': '请求成功', 'house': house.to_dict()})
    if request.method == 'POST':
        # house_title = request.form.get('house_title')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        house = House.query.get(id)
        start = datetime.strptime(start_time, '%Y-%m-%d')
        end = datetime.strptime(end_time,'%Y-%m-%d')
        orders = Order.query.filter(Order.house_id==id).all()
        is_success = 0
        if orders:
            for my_order in orders:
                if my_order.begin_date > end_time or my_order.end_date < start_time:
                    order = Order()
                    order.begin_date = start
                    order.end_date = end
                    order.days = (end - start).days
                    order.house_id = id
                    order.user_id = session['user_id']
                    order.house_price = house.price
                    order.amount = order.house_price * house.order_count

                    order.add_update()
                    is_success = 1
        else:
            order = Order()
            order.begin_date = start
            order.end_date = end
            order.days = (end - start).days
            order.house_id = id
            order.user_id = session['user_id']
            order.house_price = house.price
            order.amount = order.house_price * house.order_count
            # order.status = status
            order.add_update()
            is_success = 1
        return jsonify({'code': 200, 'msg': '请求成功', 'user_id':session['user_id'], 'success':is_success})




@order_blue.route('/orders/<int:id>/', methods=['GET'])
def orders(id):
    return render_template('orders.html')


@order_blue.route('/my_orders/<int:id>/', methods=['GET', 'POST'])
def my_orders(id):
    if request.method == 'GET':
        orders = Order.query.filter(Order.user_id==id).all()
        my_all_orders = []
        # for order in orders:
        #     my_all_orders.append(order.to_dict())
        # my_all_orders = [order.to_dict() for order in orders]
        for order in orders:
            order.amount = order.house_price * order.days
            order.comment = ''
            order.add_update()
            my_all_orders.append(order.to_dict())
        return jsonify({'code':200, 'msg': '请求成功', 'all_orders': my_all_orders})
    if request.method == 'POST':
        statu = request.form.get('statu')
        comment = request.form.get('comment')
        order_id = int(request.form.get('order_id'))
        order = Order.query.get(order_id)
        order.status = statu
        order.comment = comment
        order.add_update()
        return jsonify({'code': 200, 'msg':'请求成功', 'order': order.to_dict()})