from app import app
from flask import render_template

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

