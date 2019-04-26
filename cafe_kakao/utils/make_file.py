# -*- coding: utf-8 -*-
from collections import OrderedDict
from cafe_kakao.utils.crawl_util import build_dict, OrderedPosts
from cafe_kakao.utils.file_util import dump_output
from cafe_kakao.utils import log_util

log = log_util.Logger(__name__)


def crawl_n_make_file(**kwargs):
    post_dict = OrderedDict()
    i = 1
    while True:
        # TODO menuid없을때 exception발생원인 확인 필요
        (stop_reason, no_new_post, post_dict) = build_dict(
            post_dict,
            clubid=kwargs['clubid'],
            menuid=kwargs['menuid'],
            pageno=i,
            dict=post_dict,
            today=kwargs['today'])
        log.info('stop reason: %d, total posts %d, new posts %d',
                 stop_reason, len(post_dict), no_new_post)
        i += 1
        if stop_reason != 0:
            break
    post_list = OrderedPosts(post_dict)
    post_orderby_view = post_list.order_by('views')
    post_orderby_reply = post_list.order_by('reply')
    dump_output(kwargs['userid'], kwargs['clubid'], kwargs['menuid'],
                post_dict, post_orderby_view, post_orderby_reply)
