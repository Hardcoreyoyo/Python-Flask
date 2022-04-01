import os


from flask_login import UserMixin
from FromFlaskAppImport import app
from flask_sqlalchemy import SQLAlchemy

pjdir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(pjdir, 'data.sqlite')

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'UserRgeisters'
    Uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return self.username

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')
    #
    # @password.setter
    # def password(self, password):
    #     self.password_hash = Bcrypt.generate_password_hash(password).decode('utf8')
    #
    #
    # def check_password(self, password):
    #     """
    #     密碼驗證，驗證使用者輸入的密碼跟資料庫內的加密密碼是否相符
    #     :param password: 使用者輸入的密碼
    #     :return: True/False
    #     """
    #     return bcrypt.check_password_hash(self.password_hash, password)


# @app.route('/')
# def index():
#     db.create_all()
#     return 'ok'
#
#
# if __name__ == "__main__":
#     app.run()
