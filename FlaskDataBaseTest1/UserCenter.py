from flask import render_template
from flask_login import login_required, current_user
from FromFlaskAppImport import app
from flask import render_template, request, redirect, url_for

from Model_User import User


@app.route("/usercenter")
@login_required
def UserCenterFunc():
    UserCenterInfo_id = current_user.get_id()
    UserCenterInfo_Username = User.query.filter_by(username=UserCenterInfo_id).first()
    return render_template('UserCenter.html', UserCenterInfo=UserCenterInfo_Username)
