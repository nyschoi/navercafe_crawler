# navercafecrawling

네이버 카페 탑 조회/댓글 리스팅

## kakao talk 실행 법

1. python -m flask run
2. refresh token확인
3. sendkakaotalk에 refresh token갱신해서 python으로 실행

## TODO List

### WEB

- [ ] oauth시 반환값으로 자동으로 registration form으로 던질 수 있도록 해보자

### 크롤링

- [ ] 게시판 미지정시 Exception나오는데 정상인지 확인할 것
- [ ] today였나?지정하지 않는 경우 무한대로 gathering할 듯. 멈출 곳을 정해주자
- [x] crontab 설정 시 모듈을 못찾거나 디렉토리를 못찾거나 한다. 상대/절대 경로 문제인듯한데... 나중에 찾아보자

### 카카오

- [x] 주소를 xxx.yyy.com/cafe명/[1-9] 이런 형태로 안해주면 카카오톡 링크가 제대로 안걸림. 카톡 문제인지 확인해 보자 -> 누구 문제든 일단 name url을 리턴하는 것으로 바꾸자
- [ ] refresh token handler도 만들자
