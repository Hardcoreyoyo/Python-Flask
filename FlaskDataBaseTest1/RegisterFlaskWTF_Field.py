from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, ValidationError

from Model_User import User


class Register_WTF_Form(FlaskForm):
    user_id = StringField('UserId', render_kw={'placeholder': '請輸入帳號 : 至少8個字符,至少1個大寫字母,'
                                                        ' 1個小寫字母和1個數字,不能包含特殊字符'},
                          validators=[DataRequired(message='表格不可空白'),
                                      Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                                             message="至少8個字符,至少1個大寫字母,"
                                                     "1個小寫字母和1個數字,不能包含特殊字符")],
                          )

    email = EmailField('Email', render_kw={'placeholder': '請輸入信箱'},
                       validators=[DataRequired(message='表格不可空白')])

    password = PasswordField('Password', render_kw={'placeholder': '請輸入密碼'},
                             validators=[DataRequired(message='表格不可空白')])

    password2 = PasswordField('Password2', render_kw={'placeholder': '請再次輸入密碼'},
                              validators=[DataRequired(message='表格不可空白'),
                                          EqualTo('password', message='確認密碼與密碼不符合')])

    submit = SubmitField('送出')

    def validate_user_id(self, user_id):
        check_username = User.query.filter_by(username=user_id.data).first()
        if check_username:
            raise ValidationError('此帳號已經有人使用')

    def validate_email(self, email):
        check_email = User.query.filter_by(email=email.data).first()
        if check_email:
            raise ValidationError('此信箱已經有人使用')
