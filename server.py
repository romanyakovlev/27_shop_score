from flask import Flask, render_template, jsonify
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker, Query
import datetime
from sqlalchemy import func
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://score:Rysherat2@shopscore.devman.org:5432/shop'
db = SQLAlchemy(app)
Base = declarative_base()
Base.metadata.reflect(db.engine)

class Shop(Base):
    __table__ = Base.metadata.tables['orders']

db_session = scoped_session(sessionmaker(bind=db.engine))

server_tz = pytz.timezone('Europe/Moscow')


@app.route('/')
def score():
    orders_data = db_session.query(Shop).order_by(Shop.created.desc()).filter(Shop.status != 'DRAFT').limit(10).all()
    date_start_day = datetime.datetime.now(server_tz).replace(hour=0, minute=0, second=0, microsecond=0)
    day_process_amount = db_session.query(Shop).filter(Shop.status != 'DRAFT').filter(Shop.confirmed > date_start_day).count()
    processing_orders_count = db_session.query(Shop).filter(Shop.status == 'DRAFT').count()
    total_minutes_remaining = datetime.timedelta(seconds=0)
    if processing_orders_count != 0:
        orders_arr = db_session.query(Shop).filter(Shop.status == 'DRAFT').all()
        time_remaining = max([datetime.datetime.now(pytz.utc) - server_tz.localize(x.created).astimezone(pytz.utc)
             for x in orders_arr])
        print(time_remaining)
        total_minutes_remaining = time_remaining
        #total_minutes_remaining.microseconds = 0

    return render_template('score.html', orders_data=orders_data, timedelta_=datetime.timedelta,
                           processing_orders_count=processing_orders_count, minutes=total_minutes_remaining,
                           day_process_amount=day_process_amount)

@app.route('/get_data')
def get_data():
    date_start_day = datetime.datetime.now(server_tz).replace(hour=0, minute=0, second=0, microsecond=0)
    confirmed_orders_amount = db_session.query(Shop).filter(Shop.status != 'DRAFT').filter(Shop.confirmed > date_start_day).count()
    unconfirmed_orders_amount = db_session.query(Shop).filter(Shop.status == 'DRAFT').count()
    total_minutes_remaining = 0
    processing_orders_count = db_session.query(Shop).filter(Shop.status == 'DRAFT').count()

    if processing_orders_count != 0:
        orders_arr = db_session.query(Shop).filter(Shop.status == 'DRAFT').all()
        time_remaining = max([datetime.datetime.now(pytz.utc) - server_tz.localize(x.created).astimezone(pytz.utc)
             for x in orders_arr])
        print(time_remaining)
        total_minutes_remaining = time_remaining.seconds
    return jsonify({'confirmed_orders_amount': confirmed_orders_amount,
                    'unconfirmed_orders_amount': unconfirmed_orders_amount,
                    'total_minutes_remaining': total_minutes_remaining})


if __name__ == "__main__":
    app.run(port=5050)
