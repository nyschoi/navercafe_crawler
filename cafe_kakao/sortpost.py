# -*- coding: utf-8 -*-
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


if __name__ == "__main__":
    from testdata import a
    s = OrderedPosts(a)
    b = s.order_by('views')
    c = s.order_by('reply')
    print(s.list)
    print(b)
    print(c)
