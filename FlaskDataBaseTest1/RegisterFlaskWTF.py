from FromFlaskAppImport import app, bcrypt
from flask import Flask, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from RegisterFlaskWTF_Field import Register_WTF_Form
from Model_User import User, db


@app.route('/register/wtf', methods=['GET', 'POST'])
def Register_WTF_Def():
    form = Register_WTF_Form()
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data, method='pbkdf2:sha1', salt_length=16)
        User_Data_ckecked = User(username=form.user_id.data,
                                 email=form.email.data,
                                 password=password)
        db.session.add(User_Data_ckecked)
        db.session.commit()
        return redirect(url_for('home', check_message="註冊成功"))

    return render_template('RegisterFlaskWTF.html', form=form)


if __name__ == '__main__':
    app.run()
