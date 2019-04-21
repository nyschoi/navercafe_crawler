# -*- coding: utf-8 -*-
import glob
import os
import json
from collections import OrderedDict
import requests


def send_kakaotalk(**kwargs):
    response = getAccessTokenByRefreshToken(kwargs['rest_api_key'],
                                            kwargs['refresh_token'])
    print('getAccessTokenByRefreshToken result', response)
    print(
        'send kaTalk result(ByView) =',
        sendMessageTemplate(response['access_token'], kwargs['userid'],
                            kwargs['clubid'], kwargs['menuid'], 'ByView'))
    print(
        'send kaTalk result(ByReply) =',
        sendMessageTemplate(response['access_token'], kwargs['userid'],
                            kwargs['clubid'], kwargs['menuid'], 'ByReply'))


def sendMessageTemplate(access_token, userid, clubid, menuid, content_type):
    """기본 템플릿을 이용하여 나와의 챗팅방으로 메시지 보내기
    Arguments:
        access_token {[type]} -- [description]
        userid {[type]} -- [description]
        clubid {[type]} -- [description]
        menuid {[type]} -- [description]
        content_type {[type]} -- [description]
    Returns:
        [type] -- [description]
    """
    url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        'Authorization': "Bearer " + access_token,
    }
    if content_type == 'ByView':
        payloadDict = build_payload(userid, clubid, menuid, 'ByView')
    else:
        payloadDict = build_payload(userid, clubid, menuid, 'ByReply')
    payload = 'template_object=' + str(json.dumps(payloadDict))
    reponse = requests.request("POST", url, data=payload, headers=headers)
    result_code = json.loads(((reponse.text).encode('utf-8')))
    return result_code


def getAccessToken(redirect_url, clientId, code):
    """[summary]
    사용자 토큰 받기:
    code로 API를 호출할 수 있는 사용자 토큰(Access Token, Refresh Token)을 받아 옴
    Returns:
        [type] -- [dict]
    """
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code&client_id=" + clientId + \
        "&redirect_url=" + redirect_url + "oauth&code=" + \
        code  # payload = "grant_type=authorization_code&client_id=" + clientId + "&redirect_url=http://ec2-54-180-166-6.ap-northeast-2.compute.amazonaws.com:5000/oauth&code=" + code
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    access_token = json.loads(((response.text).encode('utf-8')))
    return access_token


def getAccessTokenByRefreshToken(rest_api_key, refresh_token):
    """refresh_token으로 AccessToken을 받아온다
    Arguments:
        refresh_token {[str]} -- [refresh_token]
    Returns:
        [str] -- [AccessToken]
    """
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=refresh_token&client_id=" + \
        rest_api_key + "&refresh_token=" + refresh_token
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    reponse = requests.request("POST", url, data=payload, headers=headers)
    access_token = json.loads(((reponse.text).encode('utf-8')))
    return access_token


def getUserInfo(access_token):
    """get user info
    Arguments:
        access_token {str} -- [Authorizatino에 access_token]
    Returns:
        [type] -- [dict]
    """
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    headers.update({'Authorization': 'Bearer ' + str(access_token)})
    url = 'https://kapi.kakao.com/v2/user/me'
    response = requests.request('POST', url, headers=headers)
    return response.text


def build_payload(userid, clubid, menuid, content_type):
    """content_type(조회/댓글순)으로 최신 파일을 읽어 카톡메시지 헤더/바디 구성)
    Arguments:
        userid {int} -- userid
        clubid {int} -- clubid
        menuid {int} -- menuid
        content_type {ByView, ByReply} -- [메시지유형]
    Returns:
        [dict] -- [카톡 메시지 헤더/바디]
    """
    if content_type == 'ByView':
        list_of_files = glob.glob('./crawl_data/' + str(userid) + '-' + str(clubid)
                                  + '-' + str(menuid) + '-views-*')
        latest_file = max(list_of_files, key=os.path.getctime)
    else:  # ByReply
        list_of_files = glob.glob('./crawl_data/' + str(userid) + '-' + str(clubid)
                                  + '-' + str(menuid) + '-reply-*')
        latest_file = max(list_of_files, key=os.path.getctime)
    print(f'latest file {content_type} : {latest_file}')
    with open(latest_file, 'r') as fout:
        datasource = json.load(fout)
    message = OrderedDict()
    if content_type == 'ByView':
        header = {
            "object_type": "list",
            "header_title": datasource[0]['boardname'] + "의 오늘 TOP 조회수 게시글",
            "header_link": {
                "web_url": datasource[0]['cafeurl'],
                "mobile_web_url": datasource[0]['cafeurl'],
            }
        }
        body = []
        for i in range(3):
            post = {
                "title": datasource[i]['title'],
                'description': '조회수' + datasource[i]['views'],
                'image_url':
                "https://cfm.kt.com/images/ir/ico-footer-sns-facebook.png",
                'link': {
                    'web_url': datasource[i]['nameurl'],
                    'mobile_web_url': datasource[i]['nameurl']
                }
            }
            body.append(post)
    else:  # ByReply
        header = {
            "object_type": "list",
            "header_title": datasource[0]['boardname'] + "의 오늘 TOP 리플 게시글",
            "header_link": {
                "web_url": datasource[0]['cafeurl'],
                "mobile_web_url": datasource[0]['cafeurl'],
            }
        }
        body = []
        for i in range(3):
            post = {
                "title": datasource[i]['title'],
                'description': '리플수' + datasource[i]['reply'],
                'image_url': "https://cfm.kt.com/images/smartTalk/bg_stit.png",
                'link': {
                    'web_url': datasource[i]['nameurl'],
                    'mobile_web_url': datasource[i]['nameurl']
                }
            }
            body.append(post)
    contents = {'contents': body}
    message.update(header)
    message.update(contents)
    return message
