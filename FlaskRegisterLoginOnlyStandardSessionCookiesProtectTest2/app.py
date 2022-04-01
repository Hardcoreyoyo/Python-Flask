import os
from datetime import timedelta, datetime

from urllib.parse import urlparse, urljoin
from flask import Flask, flash, render_template, redirect, url_for, request, abort, g, Response, make_response
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm


from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, ValidationError
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(pjdir, 'data.sqlite')
app.secret_key = 'mr87iz3fzegjy9asr'
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'Login'
login_manager.login_message = '無權限訪問此頁面﹐請重新登入'

app.config['SESSION_TYPE'] = "sqlalchemy"
app.config['SESSION_KEY_PREFIX'] = "SessionData_"
SessionExten = Session(app)
SessionExten.permanent = True
app.permanent_session_lifetime = timedelta(seconds=120)


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class UserData(db.Model):
    __tablename__ = 'UserDataTable'
    UserId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


    def __repr__(self):
        return self.username


class ipBlock(db.Model):
    __tablename__ = 'ipBlockTable'
    ipKey = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(80), unique=True, nullable=False)
    BlockTime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, ip):
        self.ip = ip

    def __repr__(self):
        return self.ip


class Register_WTF_Form(FlaskForm):
    user_id = StringField('UserId', render_kw={'placeholder': '請輸入帳號 : 至少8個字符,至少1個大寫字母,'
                                                              ' 1個小寫字母和1個數字,不能包含特殊字符'},
                          validators=[DataRequired(message='表格不可空白'),
                                      Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                                             message="至少8個字符,至少1個大寫字母,"
                                                     "1個小寫字母和1個數字,不能包含特殊字符")],
                          )

    email = EmailField('Email', render_kw={'placeholder': '請輸入信箱'},
                       validators=[DataRequired(message='表格不可空白'), Email(message='不符合信箱格式')])

    password = PasswordField('Password', render_kw={'placeholder': '請輸入密碼'},
                             validators=[DataRequired(message='表格不可空白')])

    password2 = PasswordField('Password2', render_kw={'placeholder': '請再次輸入密碼'},
                              validators=[DataRequired(message='表格不可空白'),
                                          EqualTo('password', message='確認密碼與密碼不符合')])

    submit = SubmitField('送出')

    def validate_user_id(self, user_id):
        check_username = UserData.query.filter_by(username=user_id.data).first()
        if check_username:
            raise ValidationError('此帳號已經有人使用')

    def validate_email(self, email):
        check_email = UserData.query.filter_by(email=email.data).first()
        if check_email:
            raise ValidationError('此信箱已經有人使用')


class LoginFlaskVerClass(UserMixin):
    pass


class Login_WTF_Form(FlaskForm):
    user_id = StringField('Userid', render_kw={'placeholder': '請輸入帳號'},
                          validators=[DataRequired(message='表格不可空白')])

    password = PasswordField('Password', render_kw={'placeholder': '請輸入密碼'},
                             validators=[DataRequired(message='表格不可空白')])

    submit = SubmitField('登入')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    if test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc:
        return True
    else:
        return False




@login_manager.user_loader
def user_loader(username):
    user = LoginFlaskVerClass()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(self):
    form = Login_WTF_Form()
    Check_Username_For_ID = form.user_id.data
    if Check_Username_For_ID:
        user = UserMixin()
        user.id = Check_Username_For_ID
        return user


@app.route('/')
def Home():
    return render_template('Home.html')


@app.route('/Register', methods=['GET', 'POST'])
def Register():
    form = Register_WTF_Form()
    if request.method == 'GET':
        return render_template('Register.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                User_Data_ckecked = UserData(username=form.user_id.data,
                                             email=form.email.data,
                                             password=password)
                db.session.add(User_Data_ckecked)
                db.session.commit()
            except:
                flash("註冊失敗")
                return render_template('Register.html', form=form)
            else:
                if request.args.get('next') and request.referrer:
                    for target in request.args.get('next'), request.referrer:
                        if is_safe_url(target) is True:
                            flash("註冊成功")
                            return redirect(url_for('Home'))
                        else:
                            return "Warning! Redirect Attact!"
                else:
                    flash("註冊成功")
                    return redirect(url_for('Home'))

        return render_template('Register.html', form=form)


@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'GET':
        ip = request.remote_addr
        if current_user.is_authenticated:
            current_user_username = current_user.get_id()
            flash(f' {current_user_username} 您已經登入')
            return render_template('Home.html')
        else:
            form = Login_WTF_Form()
            return render_template('Login.html', form=form)
    if request.method == 'POST':
        ip = request.remote_addr
        form = Login_WTF_Form()
        if form.validate_on_submit():
            Username_Checked = UserData.query.filter_by(username=form.user_id.data).first()
            if Username_Checked is None:
                flash('帳號或密碼輸入錯誤')
                return render_template('Login.html', form=form)
            else:
                Password_Checked = Username_Checked.password
                Password = form.password.data
                Password_hash_Checked = bcrypt.check_password_hash(Password_Checked, Password)
                if Password_hash_Checked is True:
                    user = UserMixin()
                    user.id = form.user_id.data
                    login_user(user)
                    if request.args.get('next') and request.referrer:
                        for target in request.args.get('next'), request.referrer:
                            if is_safe_url(target) is True:
                                flash('登入成功')
                                return redirect(url_for('UserCenter'))
                            else:
                                return "Warning! Redirect Attact!"
                    else:
                        flash('登入成功')
                        return redirect(url_for('UserCenter'))
                else:
                    flash('帳號或密碼輸入錯誤')
                    return render_template('Login.html', form=form)
        else:
            return render_template("Login.html", form=form)


@app.route('/UserCenter', methods=['GET', 'POST'])
@login_required
def UserCenter():
    UserCenterInfo_id = current_user.get_id()
    UserCenterInfo_Username = UserData.query.filter_by(username=UserCenterInfo_id).first()
    return render_template('UserCenter.html', UserCenterInfo=UserCenterInfo_Username)


@app.route('/Logout')
@login_required
def Logout():
    logout_user()
    if request.args.get('next') and request.referrer:
        for target in request.args.get('next'), request.referrer:
            if is_safe_url(target) is True:
                flash('登出成功')
                return redirect(url_for('Home'))
            else:
                return "Warning! Redirect Attact!"
    else:
        flash('登出成功')
        return redirect(url_for('Home'))


@app.route('/tt')
def SessionClear():
    InputDataBaseSize = 23000
    InputSessionLifeTime = 120
    InputDataBaseName = str("data.sqlite")

    App_Dir = os.path.abspath(os.path.dirname(__file__))
    DataBaseDir = os.path.join(App_Dir, InputDataBaseName)
    DataBaseSize = os.path.getsize(DataBaseDir)
    if DataBaseSize > InputDataBaseSize:
        Now = datetime.now()
        SessionDataBase = SessionExten.app.session_interface
        SessionTime = SessionDataBase.sql_session_model.query.all()
        for st in SessionTime:
            Result = Now - st.expiry
            if Result.seconds > InputSessionLifeTime and Result.days < 0:
                pass
            else:
                SessionDataid = SessionDataBase.sql_session_model.query.get(st.id)
                SessionDataBase.db.session.delete(SessionDataid)
                SessionDataBase.db.session.commit()

    return render_template('Home.html', tt="YY")


# if __name__ == "__main__":
#     app.run()

if __name__ == "__main__":
    manager.run()