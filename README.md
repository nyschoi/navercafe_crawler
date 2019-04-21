# navercafecrawling

네이버 카페 탑 조회/댓글 리스팅

## TODO List
### AWS
- [x] config.ini
- [x] sitedb복사(scp)
- [x] crontab 조정
- [ ] AWS에선 refresh token안되는 이유 찾아보기

### WEB
- [x] 404가 더럽히니 favicon만들어주자 https://www.favicon-generator.org
- [ ] oauth시 반환값으로 자동으로 registration form으로 던질 수 있도록 해보자
- [x] dev/prod환경에서 url을 깔끔히 정리

### 크롤링
- [ ] getAccessToken url손으로 고치는 것 수정하자config로되도록
- [ ] 게시판 미지정시 Exception나오는데 정상인지 확인할 것
- [ ] today였나?지정하지 않는 경우 무한대로 gathering할 듯. 멈출 곳을 정해주자
- [x] crontab 설정 시 모듈을 못찾거나 디렉토리를 못찾거나 한다. 상대/절대 경로 문제인듯한데... 나중에 찾아보자

### 카카오

- [x] 주소를 xxx.yyy.com/cafe명/[1-9] 이런 형태로 안해주면 카카오톡 링크가 제대로 안걸림. 카톡 문제인지 확인해 보자 -> 누구 문제든 일단 name url을 리턴하는 것으로 바꾸자
- [ ] refresh token handler도 만들자
