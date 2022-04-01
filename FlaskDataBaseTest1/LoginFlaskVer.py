# coding=utf-8
from datetime import timedelta
from urllib.parse import urlparse, urljoin

from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, ValidationError
from FromFlaskAppImport import app, bcrypt
from flask import Flask, render_template, redirect, url_for, request, flash, session, abort
from Model_User import User, db
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


class LoginFlaskVerClass(UserMixin):
    pass


class Login_WTF_Form(FlaskForm):
    user_id = StringField('Userid', render_kw={'placeholder': '請輸入帳號'},
                          validators=[DataRequired(message='表格不可空白')])

    password = PasswordField('Password', render_kw={'placeholder': '請輸入密碼'},
                             validators=[DataRequired(message='表格不可空白')])

    submit = SubmitField('登入')


login_manager = LoginManager()
login_manager.init_app(app)

login_manager.session_protection = "strong"
login_manager.login_view = 'Login_FlaskVer'
login_manager.login_message = '無權限訪問此頁面'


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


@app.route('/login', methods=['GET', 'POST'])
def Login_FlaskVer():
    if request.method == 'GET':
        if current_user.is_authenticated:
            current_user_username = current_user.get_id()  # current_user.get_id() 的值是 Model_User.py
            flash(f'Hi ! {current_user_username} 您已經登入')  # class 中的 def __repr__(self):    return self.username
            return redirect(url_for('home'))
        else:
            form = Login_WTF_Form()
            return render_template("LoginFlaskVer.html", form=form)
    if request.method == 'POST':
        form = Login_WTF_Form()
        if form.validate_on_submit():
            Username_Checked = User.query.filter_by(username=form.user_id.data).first()
            Password = form.password.data
            Password_Checked = Username_Checked.password
            Password_hash_Checked = check_password_hash(Password_Checked, Password)
            if Username_Checked is not None \
                    and Password_hash_Checked is True:
                user = UserMixin()
                user.id = form.user_id.data
                login_user(user)

                if request.args.get('next') and request.referrer:
                    for target in request.args.get('next'), request.referrer:
                        if is_safe_url(target) is True:
                            return redirect(url_for('UserCenterFunc'))
                        else:
                            return "你壞壞"
                else:
                    return redirect(url_for('UserCenterFunc'))

            else:
                flash('帳號或密碼輸入錯誤')
                return render_template('LoginFlaskVer.html', form=form)
        else:
            flash('form.validate_on_submit認證不過')
            return render_template("LoginFlaskVer.html", form=form)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    if test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc:
        return True
    else:
        return False


"""
為了避免被重新定向的url攻擊，必需先確認該名使用者是否有相關的權限，
舉例來說，如果使用者調用了一個刪除所有資料的uri，那就GG了，是吧 。
:param url: 重新定向的網址
:return: boolean
"""


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功')
    return render_template('Home.html')


if __name__ == '__main__':
    app.run()
