from urllib.parse import urlparse, urljoin

from flask import Flask, request, render_template, flash, redirect, url_for
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, InputRequired, Email

app = Flask(__name__)
app.secret_key = ("ssg8r48r4dfmku")


# class MyInputRequired(InputRequired):
#     field_flags = ("VVVVVVVVVVVVVVV")
#
#


class WTFormsTest1(FlaskForm):
    username = StringField('username', validators=[InputRequired(message="不准空白")])
    email = EmailField('Email',
                       validators=[InputRequired(message="不准空白"), Email(message="Email格式不對")])
    sumbit = SubmitField('GO')


# @app.route('/home', methods=['GET', 'POST'])
# def WTFormsFunc1():

@app.route('/', methods=['GET', 'POST'])
def WTFormsFunc1():
    form = WTFormsTest1()
    if request.method == 'GET':
        return render_template("WTFormFront.html", form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            u = form.username.data
            p = form.email.data
            default = "WTFormsFunc1"
            for target in request.args.get('next'), request.referrer:
                if target:
                    if is_safe_url(target):
                        u = urlparse(request.host_url)
                        u1 = u.netloc
                        p = urlparse(urljoin(request.host_url, target))
                        p1 = p.netloc
                        p2 = p.scheme
                        return render_template("DataShow.html", form=form, u=u, p=p, p1=p1, u1=u1, p2=p2)
                    else:
                        u = urlparse(request.host_url)
                        u1 = u.netloc
                        p = urlparse(urljoin(request.host_url, target))
                        p1 = p.netloc
                        p2 = p.scheme
                        x = "你壞壞"
                        return render_template("DataShow.html", form=form, x=x, u=u, p=p, p1=p1, u1=u1, p2=p2)
            return "OKOK"


        else:
            return render_template("WTFormFront.html", form=form)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    if test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc:
        return True
    else:
        return False



@app.route('/DataShow', methods=['GET', 'POST'])
def DataShow():
    return render_template("DataShow.html")


@app.route('/test1', methods=['GET', 'POST'])
def test1():
    form = WTFormsTest1()
    return render_template("WTFormFront.html", form=form)


if __name__ == '__main__':
    app.run()

# 使用StringField,EmailField等Field
# 代表使用瀏覽器預設的驗證規則以及顯示字串
# Field搭配validators的Required系列 也是會使用瀏覽器預設的驗證規則以及顯示字串
#
# 如不想使用瀏覽器預設辦法1
# 在html form 中加入 novalidate 參數
#
# <form method="POST" action="{{ url_for("WTFormsFunc1") }}" novalidate>
#
# 此時
# username = StringField('username', validators=[InputRequired(message="不准空白")])
# 中的validators 驗證規則還是可以用
#
# 如不想使用瀏覽器預設辦法2
# class MyInputRequired(InputRequired):
#      field_flags = ("這裡字串會取代瀏覽器顯示字串")
# 但如EmailField的驗證規則還是在
#
#
# validators 中的 Email驗證規則要額外安裝
# pip install email_validator
