import json
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from cafe_kakao import app, db, bcrypt
from cafe_kakao.models import User, Post
from cafe_kakao.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from cafe_kakao.utils.kakao_util import getAccessToken, getUserInfo


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    kakaoid=form.kakaoid.data, password=hashed_password, refresh_token=form.refresh_token.data, access_token=form.access_token.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(kakaoid=form.kakaoid.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check 카카오id and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.kakaoid = form.kakaoid.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.kakaoid.data = current_user.kakaoid
    return render_template('account.html', title='Account', form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(clubid=form.clubid.data, menuid=form.menuid.data,
                    description=form.description.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('즐겨찾기 추가됨!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='즐겨찾기 추가',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.description, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.clubid = form.clubid.data
        post.menuid = form.menuid.data
        post.description = form.description.data
        db.session.commit()
        flash('즐겨찾기 게시판 업데이트!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.clubid.data = post.clubid
        form.menuid.data = post.menuid
        form.description.data = post.description
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('삭제완료!', 'success')
    return redirect(url_for('home'))


@app.route('/subscribe')
def subscribe():
    server_url = app.config['SERVER_URL']
    return render_template('subscribe.html', server_url=server_url)


@app.route('/oauth')  # 코드 받기
def oauth():
    REST_API_KEY = app.config['REST_API_KEY']
    SERVER_ENV = app.config['SERVER_ENV']
    try:
        code = str(request.args.get('code'))
        resToken = getAccessToken(SERVER_ENV,
                                  REST_API_KEY, str(code))  # RESET API KEY값을 사용
        user_info = json.loads(getUserInfo(resToken['access_token']))
        text_output = 'code=' + str(code) + '<p>res Token=' + str(resToken)
        text_output += '<p>access_token=' + resToken[
            'access_token'] + '<p>refresh token=' + resToken['refresh_token']
        text_output += '<p>nickname=' + user_info['properties'][
            'nickname'] + '<p>id=' + str(user_info['id'])
    except Exception as e:
        text_output = '에러...(새로고침하지말고 back버튼 누르세영)' + str(e)
    return text_output
