from FromFlaskAppImport import app
from flask import render_template, request, redirect, url_for
from Model_User import User, db


# 最簡單功能stable
# @app.route('/register/', methods=['GET', 'POST'])
# def register(Register_Form_Data=None):
#     if request.method == 'GET':
#         return render_template('register.html', Register_Form_Data=Register_Form_Data)
#
#     if request.method == 'POST':
#         if request.form['send'] == '送出':
#
#             Register_Form_Data = [request.form['username'], request.form['userid'],
#                                   request.form['userpw'], request.form['userpw2'], request.form['useremail']]
#
#             check_username = User.query.filter_by(username=request.form['userid']).first()
#             check_email = User.query.filter_by(email=request.form['useremail']).first()
#
#             if check_username:
#                 return render_template('register.html', check_message='此帳號已有人註冊', Register_Form_Data=Register_Form_Data)
#
#             elif request.form['userpw'] != request.form['userpw2']:
#                 return render_template('register.html', check_message='密碼與確認密碼不同',
#                                        Register_Form_Data=Register_Form_Data)
#
#             elif check_email:
#                 return render_template('register.html', check_message='此信箱已有人註冊', Register_Form_Data=Register_Form_Data)
#
#             else:
#                 User_Data_ckecked = User(username=request.form['userid'],
#                                          email=request.form['useremail'], password=request.form['userpw'])
#                 db.session.add(User_Data_ckecked)
#                 db.session.commit()
#                 return redirect(url_for('home', check_message="註冊成功"))


# 最簡單功能 + 判斷表格不為空  stable
# @app.route('/register/', methods=['GET', 'POST'])
# def register(Register_Form_Data=None):
#     if request.method == 'GET':
#         return render_template('register.html', Register_Form_Data=Register_Form_Data)
#
#     if request.method == 'POST':
#         if request.form['send'] == '送出':
#
#             Register_Form_Data = [request.form['username'], request.form['userid'],
#                                   request.form['userpw'], request.form['userpw2'], request.form['useremail']]
#             check_empty_state = 1
#
#             for check_empty in Register_Form_Data:
#                 check_empty_len = len(check_empty)
#                 if check_empty_len == 0:
#                     check_empty_state = 1
#                     break
#                 else:
#                     check_empty_state = 0
#
#             if check_empty_state == 0:
#
#                 check_username = User.query.filter_by(username=request.form['userid']).first()
#                 check_email = User.query.filter_by(email=request.form['useremail']).first()
#
#                 if check_username:
#                     return render_template('register.html', check_message='此帳號已有人註冊',
#                                            Register_Form_Data=Register_Form_Data)
#
#                 elif request.form['userpw'] != request.form['userpw2']:
#                     return render_template('register.html', check_message='密碼與確認密碼不同',
#                                            Register_Form_Data=Register_Form_Data)
#
#                 elif check_email:
#                     return render_template('register.html', check_message='此信箱已有人註冊',
#                                            Register_Form_Data=Register_Form_Data)
#
#                 else:
#                     User_Data_ckecked = User(username=request.form['userid'],
#                                              email=request.form['useremail'], password=request.form['userpw'])
#                     db.session.add(User_Data_ckecked)
#                     db.session.commit()
#                     return redirect(url_for('home', check_message="註冊成功"))
#             else:
#                 return render_template('register.html', check_message='表格不為空',
#                                        Register_Form_Data=Register_Form_Data)





# 最簡單功能 + 先判斷表格不為空再同時判斷表格規則  stable
@app.route('/register/', methods=['GET', 'POST'])
def register(Register_Form_Data=None):
    if request.method == 'GET':
        return render_template('register.html', Register_Form_Data=Register_Form_Data)

    if request.method == 'POST':
        if request.form['send'] == '送出':

            Register_Form_Data = [request.form['username'], request.form['userid'],
                                  request.form['userpw'], request.form['userpw2'], request.form['useremail']]
            check_empty_state = 1

            for check_empty in Register_Form_Data:
                check_empty_len = len(check_empty)
                if check_empty_len == 0:
                    check_empty_state = 1
                    break
                else:
                    check_empty_state = 0

            if check_empty_state == 0:

                check_username = User.query.filter_by(username=request.form['userid']).first()
                check_email = User.query.filter_by(email=request.form['useremail']).first()
                Master_Message = []

                if check_username:
                    check_username_state = 1
                    check_message1 = '此帳號已有人註冊'
                    Master_Message.append(check_message1)
                else:
                    check_username_state = 0

                if request.form['userpw'] != request.form['userpw2']:
                    check_pw_state = 1
                    check_message2 = '密碼與確認密碼不同'
                    Master_Message.append(check_message2)
                else:
                    check_pw_state = 0

                if check_email:
                    check_pw_state = 1
                    check_message3 = '此信箱已有人註冊'
                    Master_Message.append(check_message3)
                else:
                    check_pw_state = 0

                if check_username_state == 0 and check_pw_state == 0 and check_pw_state == 0:
                    User_Data_ckecked = User(username=request.form['userid'],
                                             email=request.form['useremail'], password=request.form['userpw'])
                    db.session.add(User_Data_ckecked)
                    db.session.commit()
                    return redirect(url_for('home', check_message="註冊成功"))

                else:
                    return render_template('register.html',
                                           check_message=Master_Message,
                                           Register_Form_Data=Register_Form_Data)

            else:
                return render_template('register.html', check_message='表格不為空',
                                       Register_Form_Data=Register_Form_Data)


if __name__ == "__main__":
    app.run()
