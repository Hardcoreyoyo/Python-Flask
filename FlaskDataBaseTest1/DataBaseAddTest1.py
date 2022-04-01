from FromFlaskAppImport import app
from flask import Flask, render_template
from Model_Producrt import Product, db


# 新增資料至資料庫
@app.route('/a')
def CRUD1():
    a = Product(5, '', '', 6, 7)
    try:
        db.session.add(a)
        db.session.commit()
    except:
        a1 = "新增資料失敗"
        return render_template('DataBaseAddTest1.html', a1=a1)
    else:
        a2 = Product.query.all()
        a3 = "新增資料成功"
        return render_template('DataBaseAddTest1.html', a3=a3, a2=a2)


# 資料庫刪除資料
@app.route('/b')
def CRUD2():
    try:
        b = Product.query.filter_by(pid=8).first()
        db.session.delete(b)
        db.session.commit()
    except:
        b2 = "資料刪除失敗"
        return render_template('DataBaseAddTest1.html', b2=b2)
    else:
        b3 = "資料刪除成功"
        b4 = Product.query.all()
        return render_template('DataBaseAddTest1.html', b3=b3, b4=b4)


# 資料更新
@app.route('/')
def CRUD3():
    try:
        c = Product.query.get(9)
        c.pid = 8
        db.session.commit()
    except:
        c2 = "資料更新失敗"
        return render_template('DataBaseAddTest1.html', c2=c2)
    else:
        c3 = "資料更新成功"
        c4 = Product.query.all()
        return render_template('DataBaseAddTest1.html', c3=c3, c4=c4)


if __name__ == '__main__':
    app.run()
