import json
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from cafe_kakao import app, db, bcrypt
from cafe_kakao.models import User, Post, Youtube
from cafe_kakao.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, YoutubeForm
from cafe_kakao.utils.kakao_util import getAccessToken, getUserInfo
from urllib import parse
from cafe_kakao.utils import log_util
from cafe_kakao.utils import youtube_word

log_util.LogSetting.FILENAME = "./logs/app.log"
log = log_util.Logger(__name__)


@app.route("/")
@app.route("/index")
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route("/listpost")
def listpost():
    posts = Post.query.all()
    return render_template('listpost.html', posts=posts)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(clubid=form.clubid.data, menuid=form.menuid.data,
                    description=form.description.data, author=current_user)
        log.info("new favorite Posting is done:%s, %s, %s, %s", post.clubid,
                 post.menuid, post.description, current_user)
        db.session.add(post)
        db.session.commit()
        flash('즐겨찾기 추가됨!', 'success')
        return redirect(url_for('listpost'))
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
    return redirect(url_for('listpost'))


@app.route("/youtube/new", methods=['GET', 'POST'])
@login_required
def new_youtube():
    form = YoutubeForm()
    if form.validate_on_submit():
        log.info("analyzing %s", form.youtube_url.data)
        cmt_file_name, image_file = youtube_word.test(form.youtube_url.data)
        log.info("target cmt_list, image_file name :%s, %s",
                 cmt_file_name, image_file)
        post = Youtube(title=form.title.data,
                       youtube_url=form.youtube_url.data, image_file=image_file, author=current_user, comment_file=cmt_file_name)
        log.info("new Youtube Posting is done:%s, %s, %s, %s",
                 post.title, post.youtube_url, image_file, current_user)
        db.session.add(post)
        db.session.commit()
        flash('Youtube 분석 성공!', 'success')
        return redirect(url_for('listyoutube'))
    return render_template('create_youtube.html', title='분석할 Youtube 정보 입력', form=form, legend='분석할 Youtube 정보 입력')


@app.route("/youtube/<int:post_id>")
def youtube(post_id):
    post = Youtube.query.get_or_404(post_id)
    log.info("read comment file: %s", post.comment_file)
    with open('./cafe_kakao/static/wordcloud/' + post.comment_file, 'r') as f:
        comments = [line.rstrip('\n') for line in f]
    return render_template('youtube.html', title=post.title, post=post, comments=comments)


@app.route("/youtube/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_youtube(post_id):
    post = Youtube.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = YoutubeForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.youtube_url = form.youtube_url.data
        db.session.commit()
        flash('수정 완료!', 'success')
        return redirect(url_for('youtube', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.youtube_url.data = post.youtube_url
    return render_template('create_youtube.html', title='youtube 수정',
                           form=form, legend='수정하기')


@app.route("/youtube/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_youtube(post_id):
    post = Youtube.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('삭제완료!', 'success')
    return redirect(url_for('listyoutube'))


@app.route("/listyoutube")
def listyoutube():
    posts = Youtube.query.all()
    # log.info("type of posts: %s", type(posts)) # list
    return render_template('listyoutube.html', posts=posts)


@app.route('/subscribe')
def subscribe():
    server_url = app.config['SERVER_URL']
    return render_template('subscribe.html', server_url=server_url)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        log.error("validate_on_submit")
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, kakaoid=form.kakaoid.data,
                    password=hashed_password, refresh_token=form.refresh_token.data, access_token=form.access_token.data)
        db.session.add(user)
        db.session.commit()
        flash('가입이 완료되었습니다. 이제 로그인할 수 있습니다.', 'success')
        return redirect(url_for('login'))
    elif request.method == 'GET':
        form.username.data = request.args.get('username')
        form.kakaoid.data = request.args.get('kakaoid')
        form.refresh_token.data = request.args.get('refresh_token')
        form.access_token.data = request.args.get('access_token')
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    # if request.method == 'POST':  # XXX
    #     log.error("UpdateAccountForm POST %s", form.validate())

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('업데이트 완료', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/oauth')  # 코드 받기
def oauth():
    REST_API_KEY = app.config['REST_API_KEY']
    try:
        code = str(request.args.get('code'))
        resToken = getAccessToken(app.config['REDIRECT_URL'],
                                  REST_API_KEY, str(code))  # RESET API KEY값을 사용
        user_info = json.loads(getUserInfo(resToken['access_token']))
        text_output = 'code=' + str(code) + '<p>res Token=' + str(resToken)
        text_output += '<p>access_token=' + resToken[
            'access_token'] + '<p>refresh token=' + resToken['refresh_token']
        text_output += '<p>nickname=' + user_info['properties'][
            'nickname'] + '<p>id=' + str(user_info['id'])
    except Exception as e:
        text_output = '에러...(새로고침하지말고 back버튼 누르세영)' + str(e)
    # return text_output
    log.info("oauth result:%s", text_output)
    return redirect(url_for('register', username=user_info['properties']['nickname'], kakaoid=user_info['id'], refresh_token=resToken['refresh_token'], access_token=resToken['access_token']))
