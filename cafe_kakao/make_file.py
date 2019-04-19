# -*- coding: utf-8 -*-
from collections import OrderedDict
from cafe_kakao.analyze_by_page_no import build_dict
from cafe_kakao.sortpost import OrderedPosts
from cafe_kakao.dumpoutput import dump_output


def crawl_n_make_file(**kwargs):
    print()
    post_dict = OrderedDict()
    i = 1
    while True:
        # XXX menuid없을때 exception발생원인 확인 필요
        (stop_reason, no_new_post, post_dict) = build_dict(
            post_dict,
            clubid=kwargs['clubid'],
            menuid=kwargs['menuid'],
            pageno=i,
            dict=post_dict,
            today=kwargs['today'])
        print('stop reason', stop_reason, 'total posts', len(post_dict),
              'new posts', no_new_post)
        i += 1
        if stop_reason != 0:
            break
    post_list = OrderedPosts(post_dict)
    post_orderby_view = post_list.order_by('views')
    post_orderby_reply = post_list.order_by('reply')
    dump_output(kwargs['userid'], kwargs['clubid'], kwargs['menuid'],
                post_dict, post_orderby_view, post_orderby_reply)
