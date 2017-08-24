from flask import render_template, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
from main import db, app
from models import Shop
import datetime
import pytz
import os
from flask import request, send_from_directory


db_session = scoped_session(sessionmaker(bind=db.engine))
server_timezone = pytz.timezone('Europe/Moscow')
default_port = 5055


@app.route('/')
def get_page():
    return render_template('score.html')


@app.route('/get_data')
def get_data():
    max_processing_time_in_seconds = 0
    start_of_day = datetime.datetime.now(server_timezone).replace(hour=0, minute=0, second=0, microsecond=0)
    confirmed_orders_amount = db_session.query(Shop).filter(Shop.status != 'DRAFT').filter(Shop.confirmed > start_of_day).count()
    unconfirmed_orders_amount = db_session.query(Shop).filter(Shop.status == 'DRAFT').count()
    processing_orders_count = db_session.query(Shop).filter(Shop.status == 'DRAFT').count()
    if processing_orders_count is not 0:
        processing_orders_arr = db_session.query(Shop).filter(Shop.status == 'DRAFT').all()
        max_processing_time = max([datetime.datetime.now(pytz.utc) - server_timezone.localize(order.created).astimezone(pytz.utc)
                                   for order in processing_orders_arr])
        max_processing_time_in_seconds = max_processing_time.seconds
    return jsonify({'confirmed_orders_amount': confirmed_orders_amount,
                    'unconfirmed_orders_amount': unconfirmed_orders_amount,
                    'max_processing_time_in_seconds': max_processing_time_in_seconds
                    })


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


if __name__ == "__main__":
    port = int(os.environ.get('PORT', default_port))
    app.run(host='0.0.0.0', port=port)
