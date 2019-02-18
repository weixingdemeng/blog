

import redis
from flask import Flask, blueprints
from flask_script import Manager
from flask_session import Session

from aj.home_views import home_blue
from aj.models import db
from aj.order_views import order_blue
from aj.user_views import user_blue

app = Flask(__name__)

app.register_blueprint(blueprint=user_blue,url_prefix='/user')
app.register_blueprint(blueprint=order_blue,url_prefix='/order')
app.register_blueprint(blueprint=home_blue,url_prefix='/home')


# app.register_blueprint(blueprint=blue,url_prefix='/order')
# app.register_blueprint(blueprint=blue,url_prefix='/area')
# app.register_blueprint(blueprint=blue,url_prefix='/facility')
se = Session()

# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/aj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'asdfghjklqwertyuiop'
# se.init_app(app)

db.init_app(app)

manage = Manager(app)


if __name__ == '__main__':
    manage.run()