from datetime import datetime
import os, flask_login
from FromFlaskAppImport import app
from flask_sqlalchemy import SQLAlchemy

pjdir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(pjdir, 'data.sqlite')

db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = 'product'
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(30), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(
        db.String(100), unique=True, nullable=False)
    description = db.Column(
        db.String(255), nullable=False)
    state = db.Column(
        db.String(10), nullable=False)
    insert_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, onupdate=datetime.now, default=datetime.now)

    def __init__(self, name, price, img, description, state):
        self.name = name
        self.price = price
        self.img = img
        self.description = description
        self.state = state

    def __repr__(self):
        return '姓名: %s' % self.name


