<h1 align="center">
  <br>
  <a href="https://github.com/madEffort/django-traffic-server.git"><img src="https://github.com/user-attachments/assets/efb147f5-2b94-4dbb-bfbd-74b27257f2e7" alt="django-Traffic-Server-logo-color" width="400"></a>
</h1>


<h4 align="center">
django Traffic Server는 대용량 트래픽을 고려한 데이터 수집, 분석 및 모니터링을 위한 시스템으로, 각종 API 기능과 로그 처리 파이프라인을 구현하고 있습니다.</h4>


사용 기술 스택
 - Elasticsearch
 - Kibana
 - Logstash
 - MongoDB
 - PostgreSQL
 - Redis
 - Celery
 - Docker
 - RabbitMQ
 - ...

users 앱
 - JWT 방식을 이용한 로그인 기능을 적용, 로그아웃 시에는 리프레시 토큰을 블랙리스트에 등록하는 방식
 - JWT 토큰은 기본적으로 쿠키에 저장되며, iOS의 경우 쿠키를 지원하지 않아 헤더에서 토큰을 읽는 방식도 함께 적용
 - tests.py 작성 중...

boards 앱
 - 게시물 api에 transaction.atomic을 사용하여 낙관적 동시성 제어를 적용
 - 게시물을 title과 content 필드를 기준으로 elasticsearch를 적용하여 검색 가능
 - 게시물 작성 시 게시물 작성자에게 알람이 가도록 구현함
 - 게시물에 댓글 작성 시 게시물 작성자, 댓글 작성자, 게시물에 댓글을 작성한 모든 유저에게 알림이 가도록 구현함

comments 앱
- 재귀방식을 이용하여 1depth의 대댓글 기능 구현
- soft delete 방식으로 삭제 처리

campaigns 앱
 - 광고 조회 시 조회한 광고의 아이디, 유저의 id, ip주소, 조회한 시간을 MongoDB에 저장
 - 광고 클릭 시 클릭한 광고의 아이디, 유저의 id, ip주소, 클릭한 시간을 MongoDB에 저장
 - 광고에 캐싱을 적용하여 조회 시 성능 최적화
 - 저장된 데이터를 celery(beat)를 사용하여 주기적으로 집계하여 PostgreSQL에 저장

아키텍처
  
    광고 클릭 -> 클릭 로그 저장 -> MongoDB -> PostgreSQL -> Logstash -> elasticsearch -> Kibana -> [광고주 | 마케터 | 관리자]

진행 예정 

- prometheus
- kafka
- 부하테스트
