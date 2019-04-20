# -*- coding: utf-8 -*-
import time
import json
import os


def dump_output(userid, clubid, menuid, post_dict, post_orderby_view,
                post_orderby_reply):
    """수집된 결과를 파일로 저장한다
    Arguments:
        post_dict {dictionary} -- 수집된 OrderedDic
        post_orderby_view {list} -- view로 정렬된 list of dic
        post_orderby_reply {list} -- reply로 정렬된 list of dict
    """
    now = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))
    file_name = './crawl_data/' + str(userid) + '-' + str(clubid) + '-' + str(
        menuid) + '-' + 'raw-' + now + '.json'
    with open(file_name, 'w') as f:
        json.dump(post_dict, f, ensure_ascii=False)

    file_name = './crawl_data/' + str(userid) + '-' + str(clubid) + '-' + str(
        menuid) + '-' + 'views-' + now + '.json'
    with open(file_name, 'w') as f:
        json.dump(post_orderby_view, f, ensure_ascii=False)

    file_name = './crawl_data/' + str(userid) + '-' + str(clubid) + '-' + str(
        menuid) + '-' + 'reply-' + now + '.json'
    with open(file_name, 'w') as f:
        json.dump(post_orderby_reply, f, ensure_ascii=False)


def remove_crawl_data(file_path):
    if os.path.exists(file_path):
        for file in os.scandir(file_path):
            os.remove(file.path)
        return 'Rmove all file'
    else:
        return 'directory not found'
