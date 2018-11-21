from app import app
from flask import render_template, flash, redirect, url_for
from app.models import User
from flask_login import login_required, login_user, logout_user, current_user
from flask import request
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
from app import db

#导入表单处理方法
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
# @login_required
def index():
    user = {'username': 'futhead'}
    posts = [
        {
            'author': {'username': 'fuhtead'},
            'body': '载坚持3个月我就可以跑路了'

        },
        {
            'author': {'username': '漠 寒'},
            'body': '我是扶小船'
        }
    ]
    return render_template("index.html", title="我的", posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    #创建一个表单实例
    form = LoginForm()
    # 验证表格中的数据格式是否正确
    if form.validate_on_submit():
        # 根据表格里的数据进行查询，如果查询到数据返回User对象，否则返回None
        user = User.query.filter_by(username=form.username.data).first()
        # 判断用户不存在或者密码不正确
        if user is None or not user.check_password(form.password.data):
            # 如果用户不存在或者密码不正确就会闪现这条信息
            flash('无效的用户名或密码')
            # 然后重定向到登录页面
            return redirect(url_for('login'))
        # 此时的next_page记录的是跳转至登录页面是的地址
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # 这是一个非常方便的方法，当用户名和密码都正确时来解决记住用户是否记住登录状态的问题
        login_user(user, remember=form.remember_me.data)
        return redirect(next_page)
    return render_template('login.html',title='登 录',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)