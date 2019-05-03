# navercafecrawling
네이버 카페 탑 조회/댓글 리스팅

## TODO List

### 회원 관리(귀찮아서 하지 않겠다)
- [ ] 회원 탈퇴
- [ ] 아이디, 비밀번호 잊어버렸을때 찾기 기능. email 확인 절차
- [ ] 이메일 id대신 카카오id 로그인하기
### AWS
- [x] config.ini
- [x] sitedb복사(scp)
- [x] crontab 조정
- [x] logs, crawl_data directory 생성

### WEB
- [x] 404가 더럽히니 favicon만들어주자 https://www.favicon-generator.org
- [x] oauth시 반환값으로 자동으로 registration form으로 던질 수 있도록 해보자
- [x] dev/prod환경에서 url을 정리

### 크롤링
- [x] getAccessToken url손으로 고치는 것 수정하자config로되도록
- [ ] 게시판 미지정시 Exception나오는데 정상인지 확인할 것
- [ ] today였나?지정하지 않는 경우 무한대로 gathering할 듯. 멈출 곳을 정해주자
- [x] crontab 설정 시 모듈을 못찾거나 디렉토리를 못찾거나 한다. 상대/절대 경로 문제인듯한데... 나중에 찾아보자

### 카카오
- [x] 주소를 xxx.yyy.com/cafe명/[1-9] 이런 형태로 안해주면 카카오톡 링크가 제대로 안걸림. 카톡 문제인지 확인해 보자 -> 누구 문제든 일단 name url을 리턴하는 것으로 바꾸자
- [x] refresh token handler도 만들자

### youtube 댓글
- [ ] account-img만 먹는 이유가 뭔가?
- [ ] youtube 에서 \r같은 것을 지워줘야 할 듯. 이상한 데이터가 많음
- [ ] 작성자는 안나오는가?
- [ ] https://blog.goodaudience.com/how-to-generate-a-word-cloud-of-any-shape-in-python-7bce27a55f6e
- [ ] warning처리. qapplication was not...
- [ ] 127.0.0.1 - - [03/May/2019 22:22:02] "GET /youtube/new HTTP/1.1" 200 -
2019-05-03 22:22:06,198[INFO|cafe_kakao.utils.youtube_word,211] TTTESTESTSETE:55555
-------------     KT 초능력 광고    ---------------
Comments Count = 113
scan vocabs ... 
num vocabs = 2116
done = 10
WARNING: QApplication was not created in the main() thread.
2019-05-03 22:22:12.022 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.034 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.035 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.035 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.035 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.035 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.035 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.035 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.035 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.035 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.035 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.035 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
2019-05-03 22:22:12.035 python[14977:632315] pid(14977)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!
127.0.0.1 - - [03/May/2019 22:22:12] "POST /youtube/new HTTP/1.1" 302 -
127.0.0.1 - - [03/May/2019 22:22:12] "GET /listyoutube HTTP/1.1" 200 -