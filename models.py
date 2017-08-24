from main import db


class Shop(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Text)
    confirmed = db.Column(db.DateTime)
