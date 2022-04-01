from urllib.parse import urlparse, urljoin

from FromFlaskAppImport import app
from flask import render_template, request, redirect, url_for
from RegisterFlaskWTF import Register_WTF_Def
from Register import register
from LoginFlaskVer import Login_FlaskVer, logout
from UserCenter import UserCenterFunc
from StatePage import StatePage


@app.route('/')
@app.route('/<v>')
@app.route('/<path:v>')
def url_To(v=None):
    if v is None:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route('/home')
@app.route('/home/<path:check_message>', methods=['GET'])
def home(check_message=None):
    if check_message:
        return render_template('Home.html', check_message=check_message)
    else:
        return render_template('Home.html')


@app.errorhandler(405)
def page_not_found(e):
    State1 = "405是我"
    return render_template('ErrorPage1.html', State1=State1), 405


if __name__ == '__main__':
    app.run()
