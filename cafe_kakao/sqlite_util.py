from cafe_kakao import db
from cafe_kakao.models import User, Post


def drop_all():
    db.drop_all()
    db.session.commit()
    db.session.close()


def make_db():
    db.create_all()
    db.session.commit()
    db.session.close()


def create_user(**kwargs):
    """
    input: kakaoid, username, access_token, refresh_token
    output: add user
    XXX: 이미 있다면 update하는 것은 나중에 하자
    """
    user = User(kakaoid=kwargs['kakaoid'], username=kwargs['username'],
                access_token=kwargs['access_token'], refresh_token=kwargs['refresh_token'])
    db.session.add(user)
    db.session.commit()
    db.session.close()


def create_post(**kwargs):
    """
    input: clubid, menuid, kakaoid
    output: add post
    """
    post = Post(clubid=kwargs['clubid'], menuid=kwargs['menuid'],
                user_id=User.query.filter_by(kakaoid=kwargs['kakaoid']).first().id, description=kwargs['description'])
    db.session.add(post)
    db.session.commit()
    db.session.close()


# sample
if __name__ == "__main__":
    pass
