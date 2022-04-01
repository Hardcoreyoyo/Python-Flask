import os
from urllib.parse import urlparse, urljoin
from flask import Flask, flash, render_template, redirect, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, HiddenField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, ValidationError
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from threading import Thread
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature

pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(pjdir, 'data.sqlite')
app.secret_key = 'mr87iz3fzegjy9asr'
GlobalSecretKey = app.secret_key
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

login_manager.session_protection = "strong"
login_manager.login_view = 'Login'
login_manager.login_message = '無權限訪問此頁面﹐請重新登入'

app.config.update(
    DEBUG=False,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_DEFAULT_SENDER=('Flask Mail Testing', 'adgdgasdg@gmail.com'),
    MAIL_MAX_EMAILS=10,
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
)
mail = Mail(app)


class UserData(db.Model):
    __tablename__ = 'UserDataTable'
    UserId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    confirm = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password, confirm):
        self.username = username
        self.email = email
        self.password = password
        self.confirm = confirm

    def __repr__(self):
        return self.username


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


class PasswordReset_WTF_Form(FlaskForm):
    password = PasswordField('PasswordOld', render_kw={'placeholder': '請輸入原始密碼'},
                             validators=[DataRequired(message='表格不可空白')])

    password1 = PasswordField('Password1', render_kw={'placeholder': '請輸入新密碼'},
                              validators=[DataRequired(message='表格不可空白')])

    password2 = PasswordField('Password2', render_kw={'placeholder': '請再次輸入密碼'},
                              validators=[DataRequired(message='表格不可空白'),
                                          EqualTo('password1', message='確認密碼與密碼不符合')])

    submit = SubmitField('送出')

    def validate_password(self, password):
        current_user_username = UserData.query.filter_by(username=current_user.get_id()).first()
        current_user_password = current_user_username.password
        Password_hash_Checked = bcrypt.check_password_hash(current_user_password, password.data)
        if Password_hash_Checked is not True:
            raise ValidationError('原始密碼錯誤')

    def validate_password1(self, password1):
        current_user_username = UserData.query.filter_by(username=current_user.get_id()).first()
        current_user_password = current_user_username.password
        NewPassword_hash_Checked1 = bcrypt.check_password_hash(current_user_password, password1.data)
        if NewPassword_hash_Checked1 is True:
            raise ValidationError('新密碼不可與原始密碼相同')

    def validate_password2(self, password2):
        current_user_username = UserData.query.filter_by(username=current_user.get_id()).first()
        current_user_password = current_user_username.password
        NewPassword_hash_Checked2 = bcrypt.check_password_hash(current_user_password, password2.data)
        if NewPassword_hash_Checked2 is True:
            raise ValidationError('新密碼不可與原始密碼相同')


class ForgotPassword_WTF_Form(FlaskForm):
    password1 = PasswordField('Password1', render_kw={'placeholder': '請輸入新密碼'},
                              validators=[DataRequired(message='表格不可空白')])

    password2 = PasswordField('Password2', render_kw={'placeholder': '請再次輸入密碼'},
                              validators=[DataRequired(message='表格不可空白'),
                                          EqualTo('password1', message='確認密碼與密碼不符合')])

    submit = SubmitField('送出')


class ForgotPasswordEmail_WTF_Form(FlaskForm):
    email = EmailField('Email', render_kw={'placeholder': '請輸入信箱'},
                       validators=[DataRequired(message='表格不可空白'), Email(message='不符合信箱格式')])

    submit = SubmitField('送出')

    def validate_email(self, email):
        check_email = UserData.query.filter_by(email=email.data).first()
        if not check_email:
            raise ValidationError('此信箱尚未註冊')


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


@app.route('/', methods=['GET', 'POST'])
def Home():
    if request.method == 'GET':
        return render_template('Home.html')


@app.route('/ForgotPasswordEmail', methods=['GET', 'POST'])
def ForgotPasswordEmail():
    form = ForgotPasswordEmail_WTF_Form()
    if request.method == 'GET':
        if current_user.is_authenticated:
            current_user_username = current_user.get_id()
            flash(f' {current_user_username} 您已經登入')
            return redirect(url_for('UserCenter'))
        else:
            return render_template('ForgotPasswordEmail.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            URL_Serializer = TimedJSONWebSignatureSerializer(GlobalSecretKey, expires_in=300)
            Username_Serializer = UserData.query.filter_by(email=form.email.data).first()
            Username_Serializer = Username_Serializer.username
            URL_Serializer = URL_Serializer.dumps({'username': Username_Serializer})

            msg_title = "Flask測試忘記密碼認證信件"
            msg_recipients = [form.email.data]
            URL = url_for('ForgotPasswordConfirm', Key=URL_Serializer, _external=True)
            msg_html = "<h1> 您的帳號為: " + Username_Serializer + "</h1>"\
                                                              "<br><br><br>"\
                                                              "<h1>" \
                                                              "<a href= " + URL + ">啟動修改密碼</a>" \
                                                                                  "</h1>"

            msg = Message(msg_title,
                          recipients=msg_recipients)
            msg.html = msg_html

            try:
                thr = Thread(target=send_async_email, args=[app, msg])
                thr.start()
            except:
                flash("寄信失敗")
                return redirect(url_for('Home'))
            else:
                flash("寄信成功")
                return redirect(url_for('Home'))
        else:
            return render_template("ForgotPasswordEmail.html", form=form)


@app.route('/ForgotPasswordConfirm/<Key>', methods=['GET', 'POST'])
def ForgotPasswordConfirm(Key):
    form = ForgotPassword_WTF_Form()
    if request.method == 'GET':
        if current_user.is_authenticated:
            current_user_username = current_user.get_id()
            flash(f' {current_user_username} 您已經登入')
            return redirect(url_for('UserCenter'))
        else:
            s = TimedJSONWebSignatureSerializer(GlobalSecretKey)
            try:
                data = s.loads(Key)
            except SignatureExpired:
                return "Token超時"
            except BadSignature:
                return "Token驗證失敗"
            else:
                return render_template('ForgotPassword.html', form=form, Key=Key)

    if request.method == 'POST':
        if form.validate_on_submit():
            s = TimedJSONWebSignatureSerializer(GlobalSecretKey)
            try:
                data = s.loads(Key)
            except SignatureExpired:
                return "Token超時"
            except BadSignature:
                return "Token驗證失敗"
            except:
                return "TOKEN出問題"
            else:
                try:
                    username = UserData.query.filter_by(username=data.get('username')).first()
                    username.password = form.password1.data
                    db.session.commit()
                except:
                    return "資料庫資料更新失敗"
                else:
                    if request.args.get('next') and request.referrer:
                        for target in request.args.get('next'), request.referrer:
                            if is_safe_url(target) is True:
                                flash('密碼更改成功  請使用新密碼登入')
                                return redirect(url_for('Login'))
                            else:
                                return "Warning! Redirect Attact!"
                    else:
                        flash('密碼更改成功  請使用新密碼登入')
                        return redirect(url_for('Login'))
        else:
            return render_template('ForgotPassword.html', form=form)


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
                                             password=password,
                                             confirm=False)
                db.session.add(User_Data_ckecked)
                db.session.commit()
            except:
                flash("註冊失敗")
                return render_template('Register.html', form=form)
            else:
                URL_Serializer = TimedJSONWebSignatureSerializer(GlobalSecretKey, expires_in=300)
                PrimaryKey_Serializer = UserData.query.filter_by(username=form.user_id.data).first()
                PrimaryKey_Serializer = PrimaryKey_Serializer.UserId
                URL_Serializer = URL_Serializer.dumps({'UserId': PrimaryKey_Serializer})

                msg_title = "Flask測試認證信"
                msg_recipients = [form.email.data]
                Mail_Body = url_for('user_confirm', token=URL_Serializer, _external=True)
                msg = Message(msg_title,
                              recipients=msg_recipients)
                msg.body = Mail_Body

                try:
                    thr = Thread(target=send_async_email, args=[app, msg])
                    thr.start()
                except:
                    flash("寄信失敗")
                    return render_template('Home.html')
                else:
                    flash("寄信成功")
                    return render_template('Home.html')

        flash("表格認證失敗")
        return render_template('Register.html', form=form)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


@app.route('/user_confirm/<token>')
def user_confirm(token):
    if request.method == 'GET':
        if current_user.is_authenticated:
            current_user_username = current_user.get_id()
            flash(f' {current_user_username} 您已經登入')
            return render_template('Home.html')
        else:

            s = TimedJSONWebSignatureSerializer(GlobalSecretKey)
            try:
                data = s.loads(token)
            except SignatureExpired:
                return "Token超時"
            except BadSignature:
                return "Token驗證失敗"
            else:
                try:
                    user = UserData.query.filter_by(UserId=data.get('UserId')).first()
                    user.confirm = True
                    db.session.add(user)
                    db.session.commit()
                except:
                    return "資料庫帳號狀態更新失敗"
                else:
                    if request.args.get('next') and request.referrer:
                        for target in request.args.get('next'), request.referrer:
                            if is_safe_url(target) is True:
                                flash('註冊成功')
                                return redirect(url_for('Home'))
                            else:
                                return "Warning! Redirect Attact!"
                    else:
                        flash('註冊成功')
                        return redirect(url_for('Home'))


@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            current_user_username = current_user.get_id()
            flash(f' {current_user_username} 您已經登入')
            return render_template('Home.html')
        else:
            form = Login_WTF_Form()
            return render_template('Login.html', form=form)
    if request.method == 'POST':
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


@app.route('/PasswordReset', methods=['GET', 'POST'])
@login_required
def PasswordReset():
    form = PasswordReset_WTF_Form()
    if request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('PasswordReset.html', form=form)
        else:
            return redirect(url_for('Login'))

    if request.method == 'POST':
        if form.validate_on_submit():
            password = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
            current_user_username = UserData.query.filter_by(username=current_user.get_id()).first()
            current_user_username.password = password
            db.session.commit()
            logout_user()
            flash('修改成功  請使用新密碼重新登入')
            return redirect(url_for('Login'))

        return render_template('PasswordReset.html', form=form)


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


if __name__ == "__main__":
    app.run()
