from FromFlaskAppImport import app
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


#
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.session_protection = "strong"
# login_manager.login_view = 'login'
# login_manager.login_message = '您無權限訪問此網頁'
#
# @login_manager.user_loader
# def user_loader(Uid):
#     if 使用者 not in users:
#         return
#
#     user = User()
#     user.id = 使用者
#     return user


@app.route('/app123')
def app123():
    return render_template('app.html')
