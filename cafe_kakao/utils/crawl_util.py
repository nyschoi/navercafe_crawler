# -*- coding: utf-8 -*-
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup
from cafe_kakao.utils.log_util import app_log


def build_dict(post_dict, **kwargs):
    """url에 html을 파싱해서, 크롤링 정보(조회/댓글수) 포함 사전 저장
    Arguments:
        clubid -- 카페ID
        menuid -- 게시판번호
        pageno -- 페이지번호
    Returns:
        stop_reason: 수집 중지 이유. 0(성공), -1(2일이전), -2(이미 수집), 
        no_of_newly_collected: 새롭게 수집된 posts 수
        OrderedDict -- 분석된 결과 사전
    """
    # 'https://m.cafe.naver.com/ArticleAllListAjax.nhn' 못생긴 페이지가 나옴
    # https://m.cafe.naver.com/ArticleList.nhn  페이지1로만 간다?
    base_url = 'https://m.cafe.naver.com/ArticleList.nhn'
    if 'menuid' not in kwargs:
        kwargs['menuid'] = None
    if kwargs['today']:
        # day_b4_yesterday = (date.today() - timedelta(2)).strftime('%y.%m.%d')
        day_b4_yesterday = (date.today() - timedelta(1)
                            ).strftime('%y.%m.%d')  # 어제일자까지만 뽑자 괜히 길기만 하다
    params = {
        'search.clubid': kwargs['clubid'],
        'search.menuid': kwargs['menuid'],
        'search.page': kwargs['pageno'],
    }
    response = requests.get(base_url, params=params)
    # print('Analyzing...:', response.request.url)
    app_log.info('Progress:%s', response.request.url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    cafe_name = soup.select('header h1')[0].find(
        'a')['href']  # found !!!! '/biketravelers'
    no_of_newly_collected = 0
    for tag in soup.select('.list_area li'):
        try:
            post_url = tag.find('a')['href']
            article_id = tag.find('a')['data-article-id']
            cafe_url = 'https://m.cafe.naver.com' + cafe_name
            post_full_url = base_url + post_url
            post_id_url = cafe_url + '/' + article_id
            cafe_board_name = soup.select('head')[0].find('title').text.split(
                ':')[0].strip() + "/" + soup.select(
                    '#navigation .tap_area .ellip')[0].text.strip()
            post_title = ' '.join(tag.find(class_='tit').text.split())
            post_time = tag.find(class_='time').text.strip('.')
            post_views = tag.find(class_='no').text
            post_reply = tag.find(class_='link_comment').find('em').text
            istoday = ":" in post_time
            if istoday:
                pass
            elif kwargs['today'] and (post_time < day_b4_yesterday):
                # too old post(reached the day before yesterday)
                return (-1, no_of_newly_collected, post_dict)
            if post_url in post_dict:  # already have it!
                return (-2, no_of_newly_collected, post_dict)
            post_item = {
                'title': post_title,
                'time': post_time,
                'cafeurl': cafe_url,
                'views': post_views,
                'reply': post_reply,
                'nameurl': post_id_url,
                'boardname': cafe_board_name,
            }
            post_dict[post_url] = post_item
            no_of_newly_collected += 1
        except Exception as e:
            print('Exeption!!!:', e)
            continue
    return (0, no_of_newly_collected, post_dict)


class OrderedPosts:
    """Post를 입력받은 기준에 따라 소팅한다.
    입력값은 수집한 dict형 게시글
    Returns:
        __init__ -- 초기화. 반환없음. 이후 소팅을 위해 입력받은 dict을 self.list type으로 저장
        order_by(criterion) -- dispatcher. 호출에 따라 정렬된 Post를 list형태로 return
    """

    def __init__(self, dict):
        self.list = [post for post in dict.values()]

    def order_by(self, criterion):
        default = "Incorrect criterion(views, reply)"
        dispatch_func = getattr(self,
                                'orderby_' + criterion, lambda: default)()
        return dispatch_func

    def orderby_views(self):
        ordered_post = sorted(
            self.list,
            key=lambda k: int(k['views'].replace(
                ',', '').replace('만', '0000')),
            reverse=True)
        return ordered_post

    def orderby_reply(self):
        ordered_post = sorted(
            self.list,
            key=lambda k: int(k['reply'].replace(',', '')),
            reverse=True)
        return ordered_post
