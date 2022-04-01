# WTF 跳出訊息文字編輯
# hack 密碼加密
# 個網頁權限瀏覽設定
# flash 方法
# 記住我


from datetime import timedelta

from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_babel import Babel
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
import os

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, InputRequired, Length

app = Flask(__name__)
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.secret_key = '151wegweg56165164gy'
app.permanent_session_lifetime = timedelta(minutes=960)
app.REMEMBER_COOKIE_DURATION = timedelta(minutes=960)

pjdir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(pjdir, 'data.sqlite')

db = SQLAlchemy(app)


class UserData(db.Model):
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


class Login_WTF_Form(FlaskForm):
    user_id = StringField('Userid', render_kw={'placeholder': '請輸入帳號'}, validators=[InputRequired(message="PPPPPPPPP")])

    password = PasswordField('Password', render_kw={'placeholder': '請輸入密碼'},
                             validators=[InputRequired(message='表格不可空白')])
    fuck = StringField('Password2', validators=[DataRequired(), Length(min=8, max=13, message="SSSSSSSS")])
    submit = SubmitField('登入')

    # class Meta:
    #     locales = False
    #     # locales = ('zh', 'en')
    #     cache_translations = False


login_manager = LoginManager()
login_manager.init_app(app)

login_manager.session_protection = "strong"
login_manager.login_view = 'Login_FlaskVer'
login_manager.login_message = '無權限訪問此頁面'


@login_manager.user_loader
def user_loader(username):
    Check_Username_For_ID = UserData.query.filter_by(username=username).first()
    if Check_Username_For_ID is not None:
        user = UserMixin()
        user.id = Check_Username_For_ID
        return user


@login_manager.request_loader
def request_loader(self):
    form = Login_WTF_Form()
    Check_Username_For_ID = UserData.query.filter_by(username=form.user_id.data).first()
    if Check_Username_For_ID is not None:
        user = UserMixin()
        user.id = Check_Username_For_ID
        return user


@app.route('/login', methods=['GET', 'POST'])
def Login_FlaskVer():
    form = Login_WTF_Form()
    if request.method == 'GET':
        if current_user.is_authenticated:
            current_user_username = current_user.get_id()  # current_user.get_id() 的值是 Model_User.py
            flash(f'Hi ! {current_user_username} 您已經登入')  # class 中的 def __repr__(self):    return self.username
            return redirect(url_for('home'))
        else:
            return render_template("LoginFlaskVer.html", form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            Username_Checked = UserData.query.filter_by(username=form.user_id.data).first()
            Password_Checked = UserData.query.filter_by(
                username=form.user_id.data).filter_by(password=form.password.data).first()
            if Username_Checked is not None and Password_Checked is not None:
                user = UserMixin()
                user.id = form.user_id.data
                login_user(user, remember=True)
                flash('登入成功')
                session.permanent = True
                return redirect(url_for('UserCenterFunc'))
            else:
                flash('帳號或密碼輸入錯誤')
                return render_template('LoginFlaskVer.html', form=form)
        else:
            flash('請重新登入')
            return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功')
    return render_template('Home.html')


@app.route("/usercenter")
@login_required
def UserCenterFunc():
    UserCenterInfo_id = current_user.get_id()
    UserCenterInfo_Username = UserData.query.filter_by(username=UserCenterInfo_id).first()
    return render_template('UserCenter.html', UserCenterInfo=UserCenterInfo_Username)


@app.route('/')
def home():
    return render_template('Home.html')


if __name__ == '__main__':
    app.run()
