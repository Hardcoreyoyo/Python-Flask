from FromFlaskAppImport import app
from flask import Flask, render_template
from Model_Producrt import Product, db
from Model_User import User, db


# 查詢指定個別直的欄位數值
@app.route('/a')
def Find1():
    Find1 = Product.query.with_entities(Product.price)
    Find2 = Product.query.with_entities(Product.name)
    return render_template('DataBaseQueryTest1.html', Find1=Find1, Find2=Find2)


# 查詢全部 需要再HTML迭代出來
@app.route('/b')
def Find2():
    a = Product.query.all()
    return render_template('DataBaseQueryTest1.html', a=a)


#  filter_by  方法
@app.route('/c')
def Find3():
    c = Product.query.filter_by(name="Tri").first()
    # c1 = Product.query.name.first()
    return render_template('DataBaseQueryTest1.html', c=c)


#  order_by   遞增 遞減 方法
@app.route('/d')
def Find4():
    d = Product.query.order_by(Product.price)
    d2 = Product.query.order_by(Product.price.desc())
    return render_template('DataBaseQueryTest1.html', d=d, d2=d2)


#  搜尋 by primary key 方法
@app.route('/e')
def Find5():
    e = Product.query.get(6)
    # # IDIDI = User()
    # # e1 = User.id
    # idid = "test1"
    # e1 = User.get(idid)
    return render_template('DataBaseQueryTest1.html', e=e, e1=e1)


#  不同於 filter_by   在 filter 方法中 支持更多複雜的條件搜尋
@app.route('/f')
def Find6():
    f = Product.query.filter(Product.price < 10000)
    f2 = Product.query.filter(Product.description.endswith('3'), Product.price < 12000)
    return render_template('DataBaseQueryTest1.html', f=f, f2=f2)


# 判斷查詢值是否為空
# filter_by 與 filter 不同
# @app.route('/')
# def Find7():
# g = Product.query.filter_by(price=9999)
# if g is None:
#     k = "沒有找到資料"
#     return render_template('DataBaseQueryTest1.html', k=k)
# else:
#     return render_template('DataBaseQueryTest1.html', g=g)


# --------------------------------------------------------------------------


# g = Product.query.filter(Product.price < 1000)
# g2 = []

# for x in g:
#     g2.append(x)
# g3 = len(g2)
#
# if g3 == 0:
#     k = "沒有"
#     return render_template('DataBaseQueryTest1.html', k=k)
# else:
#     k = "有找到資料"
#     return render_template('DataBaseQueryTest1.html', k=k, g=g)


if __name__ == '__main__':
    app.run()
