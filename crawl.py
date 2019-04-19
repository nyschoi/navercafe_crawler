# -*- coding: utf-8 -*-
from cafe_kakao import REST_API_KEY
from cafe_kakao.make_file import crawl_n_make_file
from cafe_kakao.kakaohandler import send_kakaotalk
from cafe_kakao.models import Post


for item in Post.query.all():
    userid = item.author.kakaoid
    clubid = item.clubid
    menuid = item.menuid
    crawl_n_make_file(userid=userid, clubid=clubid, menuid=menuid, today=True)

for item in Post.query.all():
    userid = item.author.kakaoid
    clubid = item.clubid
    menuid = item.menuid
    refresh_token = item.author.refresh_token
    access_token = item.author.access_token
    send_kakaotalk(
        userid=userid,
        clubid=clubid,
        menuid=menuid,
        refresh_token=refresh_token,
        rest_api_key=REST_API_KEY)
