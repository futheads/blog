from datetime import datetime

from flask import render_template, flash, redirect, url_for, abort
from flask import request
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse

from app import app
from app import db
from app.emails import follower_notification
from app.forms import EditProfileForm
# 导入表单处理方法
from app.forms import LoginForm
from app.forms import RegistrationForm, PostForm
from app.models import User, Post
from config import Config


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page = 1):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post is now live!")
        return redirect(url_for("index"))
    posts = current_user.followed_posts().paginate(page, Config.POSTS_PER_PAGE, False)
    return render_template("index.html", title="主页", form=form,  posts=posts)

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
        # make the user follow him/herself
        db.session.add(user.follow(user))
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)

@app.route('/user/<username>')
@app.route('/user/<username>/<int:page>')
@login_required
def user(username, page=1):
    user = User.query.filter_by(username=username).first_or_404()
    if user is None:
        flash("User %s not found." % username)
        return  redirect(url_for("index"))
    posts = user.posts.paginate(page, Config.POSTS_PER_PAGE, False)
    return render_template('user.html',user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('你的提交已变更.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='个人资料编辑', form=form)

@app.route("/follow/<username>")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    if user == current_user:
        flash('You can\'t follow yourself!')
        return redirect(url_for("user", username=username))
    u = current_user.follow(user)
    if u is None:
        flash('Cannot follow ' + username + '.')
        return redirect(url_for("user", username=username))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + username + '!')
    follower_notification(user, current_user)
    return redirect(url_for("user", username=username))

@app.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("User %s not found." % username)
        return redirect(url_for("index"))
    if user == current_user:
        flash("You cann't unfollow yourself!")
        redirect(url_for("user", username=username))
    u = current_user.unfollow(user)
    if u is None:
        flash("Cannot unfollow " +username + ".")
        redirect(url_for("user", username=username))
    db.session.add(u)
    db.session.commit()
    flash("You have stopped following " + username + ".")
    return redirect(url_for("user", username=username))

@app.route("/test_error")
def test():
    abort(404)

