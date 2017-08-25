from main import db


class Shop(db.Model):

    __tablename__ = 'orders'

    status = db.Column(db.Text)
    confirmed = db.Column(db.DateTime, primary_key=True)
