#from konlpy.tag import Twitter
#from collections import Counter

#import matplotlib.pyplot as plt
#import matplotlib
#from matplotlib import font_manager, rc

#import pytagcloud
#import webbrowser


# cys
import logging
import time
from cafe_kakao.utils import log_util
log = log_util.Logger(__name__)
log.setLevel(logging.DEBUG)

# -------------------------------------------------------------------
import json
import sys
from urllib import *
import argparse
from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import urlopen


YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
YOUTUBE_COMMENT_MAX = 100
GOOGLE_API_KEY = 'AIzaSyDlGT-J97YNlHVDpzR1042Nrfm2tqRNDm0'


# cmt_list = []


def open_url(url, parms):
    #print('url = '+url)
    #print('parms = '+str(parms))
    f = urlopen(url + '?' + urlencode(parms))
    data = f.read()
    f.close()
    matches = data.decode("utf-8")
    return matches


def load_comments(mat):
    cmt_list = []
    for item in mat["items"]:
        try:
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            #print("Comment : " + text)
            cmt_list.append(text)

            # if 'replies' in item.keys():
            #    for reply in item['replies']['comments']:
            #        rauthor = reply['snippet']['authorDisplayName']
            #        rtext = reply["snippet"]["textDisplay"]
            #
            #    print("\n\tReply by {}: {}".format(rauthor, rtext), "\n")
        except:
            print("Invalid Character")
            print(str(e))


def get_video_comment(videourl):
    vid = str()

    try:
        video_id = urlparse(str(videourl))
        q = parse_qs(video_id.query)
        vid = q["v"][0]
    except:
        print("Invalid YouTube URL")

    parms = {
        'part': 'snippet,replies',
                'maxResults': YOUTUBE_COMMENT_MAX,
                'videoId': vid,
                'textFormat': 'plainText',
                'key': GOOGLE_API_KEY
    }

    try:
        matches = open_url(YOUTUBE_COMMENT_URL, parms)
        i = 2
        mat = json.loads(matches)
        nextPageToken = mat.get("nextPageToken")
        #print("\nPaging처리 : 1")
        # print("------------------------------------------------------------------")
        load_comments(mat)

        while nextPageToken:
            parms.update({'pageToken': nextPageToken})
            matches = open_url(YOUTUBE_COMMENT_URL, parms)
            mat = json.loads(matches)
            nextPageToken = mat.get("nextPageToken")
            #print("\nPaging처리 : ", i)
            # print("------------------------------------------------------------------")

            load_comments(mat)

            i += 1
    except KeyboardInterrupt:
        print("User Aborted the Operation")

    except:
        print("Cannot Open URL or Fetch comments at a moment")
        print(str(e))


# -------------------------------------------------------------------
# KRWordRank : https://lovit.github.io/nlp/2018/04/16/krwordrank/
from krwordrank.word import KRWordRank
from krwordrank.hangle import normalize


def rank_word(texts_array):
    # debug
    #print("size = " + str(len(texts_array)))
    #print(*texts_array, sep = "\n")

    wordrank_extractor = KRWordRank(
        min_count=1,   # 단어의 최소 출현 빈도수 (그래프 생성 시)
        max_length=10,  # 단어의 최대 길이
        verbose=True
    )

    beta = 0.85    # PageRank의 decaying factor beta
    max_iter = 10

    # normalize 함수는 불필요한 특수기호를 제거하는 전처리 함수
    # english=True, number=True 를 입력하면 한글, 영어, 숫자를 제외한 다른 글자를 제거
    # Default 는 english=False, number=False
    texts_array = [normalize(text, english=False, number=False)
                   for text in texts_array]

    keywords, rank, graph = wordrank_extractor.extract(
        texts_array, beta, max_iter)

    # for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:30]:
    #    print('word - %8s:\t%.4f' % (word, r))

    return keywords


# -------------------------------------------------------------------
# WordCloud : https://lovit.github.io/nlp/2018/04/17/word_cloud/
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def build_wourdcloud(word_ranking, mask_file, save_file):
    # cys
    # font_path = 'C:/STEM/malgun.ttf'
    font_path = './cafe_kakao/static/AppleGothic.ttf'
    # img_mask = np.array(Image.open('C:/STEM/' + mask_file))
    # img_mask = np.array(Image.open('./' + mask_file))

    wordcloud = WordCloud(
        font_path=font_path,
        width=800,  # 이미지크기
        height=800,
        # background_color="yellow",
        # mask = img_mask, # imaging masking
        # prefer_horizontal = 0.9999, # horizontal preference
        # min_font_size = 10 # min font size
    )

    #wordcloud = wordcloud.generate_from_text(texts)
    wordcloud = wordcloud.generate_from_frequencies(word_ranking)

    array = wordcloud.to_array()
    # print(type(array)) # numpy.ndarray
    # print(array.shape) # (800, 800, 3)

    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes([0, 0, 1, 1])
    plt.imshow(array, interpolation="bilinear")
    plt.axis("off")
    # plt.show()
    fig.savefig(save_file)


# ---------------------------  M a i n ------------------------------

def test(you_urls):
    log.info('TTTESTESTSETE:%s', you_urls)
    cmt_list.clear()

    url_list = you_urls.split(';')
    for url in url_list:
        get_video_comment(url.strip())

    print('Comments Count = ' + str(len(cmt_list)))
    #print(*cmt_list, sep = "\n")
    keywords = rank_word(cmt_list)

    now = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))
    # cmt_file_name = './cafe_kakao/wordcloud/' + 'comment-' + now + '.txt'
    # img_file_name = './cafe_kakao/wordcloud/' + 'comment-' + now + '.png'
    cmt_file_name = 'comment-' + now + '.txt'
    img_file_name = 'comment-' + now + '.png'
    build_wourdcloud(keywords, './cafe_kakao/static/alice_mask.png',
                     './cafe_kakao/static/wordcloud/' + img_file_name)
    with open('./cafe_kakao/static/wordcloud/' + cmt_file_name, 'w') as f:
        for item in cmt_list:
            f.write("%s\n" % item)
    return (cmt_file_name, img_file_name)

##    print('-------------     KT 초능력 광고    ---------------')
# [당신의 초능력 KT 5G] 런칭편
# get_video_comment('https://www.youtube.com/watch?v=4Gk2-A9lLW0')
# [당신의 초능력 KT 5G] 5G 네트워크편
# get_video_comment('https://www.youtube.com/watch?v=-b6IExXYrNM')
# [당신의 초능력 KT 5G] 이런 요금제는 없었다 5G 완전 무제한
# get_video_comment('https://www.youtube.com/watch?v=W-awGXZPMHM')
# [당신의초능력 KT 5G] 갤럭시 S10 5G도 KT에서 (슈퍼체인지)
# get_video_comment('https://www.youtube.com/watch?v=XSHQTurYYfs')
# [당신의 초능력 KT 5G] 직관보다 더 실감나게 야구를 즐기는 초능력?! KT 5G 프로야구 Live
# get_video_comment('https://www.youtube.com/watch?v=MEOmbGWfw-8')


# cmt_list.clear()
# print('-------------    SKT 초시대 광고    ---------------')
# get_video_comment('https://www.youtube.com/watch?v=72zQZ1uJosk') #[SK텔레콤] 초시대의 초5G 생활_속도 편
# get_video_comment('https://www.youtube.com/watch?v=yvU0LkgjyII') #[SK텔레콤] 초시대, 생활이 되다_초생활 편
# get_video_comment('https://www.youtube.com/watch?v=it30hx6d9tg') #[SK텔레콤] 초시대의 초5G생활_소셜VR 편
# get_video_comment('https://www.youtube.com/watch?v=3NMAECED4T0') #[SK텔레콤] 초시대의 초5G생활_소셜VR 2편
# get_video_comment('https://www.youtube.com/watch?v=didpsY9Qepg') #[SK텔레콤] 초시대의 응원 생활_빠른중계
##
##    print('Comments Count = ' + str(len(cmt_list)))
##    print(*cmt_list, sep = "\n")
##    keywords = rank_word(cmt_list)
##    build_wourdcloud(keywords, 'alice_mask.png', 'wc_api_skt.png')
