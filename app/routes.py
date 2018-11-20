from app import app
from flask import render_template, flash, redirect, url_for

#导入表单处理方法
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
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
    return render_template("index.html", title="我的", user=user, posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    #创建一个表单实例
    form = LoginForm()
    # 验证表格中的数据格式是否正确
    if form.validate_on_submit():
        # 闪现的信息会出现在页面，当然在页面上要设置
        flash('用户登录的名户名是:{} , 是否记住我:{}'.format(form.username.data, form.remember_me.data))
        # 重定向至首页
        return redirect(url_for('index'))
        # 首次登录/数据格式错误都会是在登录界面
    return render_template('login.html',title='登 录',form=form)

