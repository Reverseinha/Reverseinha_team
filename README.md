## ✒️ API

### 사용자 인증관리
| 기능         | method | REST API              | 입력 data                 | 반환 data                  |
|--------------|--------|-----------------------|---------------------------|----------------------------|
| 회원가입     | post   | /with/signup/         |                           | 성공: 200, ok 실패: 400    |
| 로그인       | post   | /with/login/          |                           | 성공: 200, ok 실패: 400    |
| 로그아웃     | post   | /with/logout/         |                           | 성공: 200, ok 실패: 400    |
| 설문조사 제출 | post   | /with/signup/survey/  |                           | 성공: 200, ok 실패: 400    |

### 커뮤니티
| 기능                 | method | REST API                                             | 입력 data                 | 반환 data                   |
|----------------------|--------|------------------------------------------------------|---------------------------|-----------------------------|
| 게시글 생성          | post   | /with/community/                                     |                           | 성공: 200, ok 실패: 400     |
| 게시글 제목검색      | get    | /with/community/search/                              |                           | 성공: 200, ok 실패: 400     |
| 특정 게시글 조회     | get    | /with/community/int:<int:pk>/                        |                           | 성공: 200, ok 실패: 404     |
| 전체 게시글 조회     | get    | /with/community/all/                                 |                           | 성공: 200, ok 실패: 400     |
| 댓글 작성            | post   | /with/community/int:<int:post_pk>/comment/           |                           | 성공: 200, ok 실패: 400     |
| 댓글 가져오기        | get    | /with/community/int:<int:post_pk>/comments/all/      |                           | 성공: 200, ok 실패: 404     |
| 댓글 삭제            | delete | /with/community/int:<int:post_pk>/comments/int:<int:pk>/delete/ |                        | 성공: 200, ok 실패: 400, 403|
| 댓글 수정            | put    | /with/community/int:<int:post_pk>/comments/int:<int:pk>/update/ |                        | 성공: 200, ok 실패: 400, 403|

### 사용자 정보
| 기능                  | method | REST API                  | 입력 data                 | 반환 data                   |
|-----------------------|--------|---------------------------|---------------------------|-----------------------------|
| 사용자 ID 조회        | get    | /with/user/id/            |                           | 성공: 200, ok 실패: 404     |
| 사용자 닉네임 조회    | get    | /with/user/nickname/      |                           | 성공: 200, ok 실패: 404     |

### 캘린더
| 기능                       | method | REST API                                      | 입력 data                 | 반환 data                   |
|----------------------------|--------|-----------------------------------------------|---------------------------|-----------------------------|
| 목표 및 일기 조회          | get    | /with/calendar/goal_diary/?date=날짜          |                           | 성공: 200, ok 실패: 404     |
| 목표 생성                  | post   | /with/calendar/goal/create/                   |                           | 성공: 200, ok 실패: 400     |
| 목표 삭제                  | delete | /with/calendar/goal/int:<int:pk>/delete/      |                           | 성공: 200, ok 실패: 404     |
| 목표 완료 상태 업데이트    | patch   | /with/calendar/goal/int:<int:pk>/completed/   |                           | 성공: 200, ok 실패: 400, 404|
| 일기 생성                  | post   | /with/calendar/diary/create/                  |                           | 성공: 200, ok 실패: 400     |
| 일기 수정                  | post   | /with/calendar/diary/update/                  |                           | 성공: 200, ok 실패: 400     |
| 일기 삭제                  | delete | /with/calendar/diary/int:<int:pk>/delete/     |                           | 성공: 200, ok 실패: 404     |

### 상담신청
| 기능                | method | REST API           | 입력 data                 | 반환 data                   |
|---------------------|--------|--------------------|---------------------------|-----------------------------|
| 상담 작성하기       | post   | /with/consulting/application/  |                           | 성공: 200, ok 실패: 400     |

### 마이페이지
| 기능                | method | REST API           | 입력 data                 | 반환 data                   |
|---------------------|--------|--------------------|---------------------------|-----------------------------|
| 마이페이지           | get    | /with/mypage/      |                           | 성공: 200, ok 실패: 404     |
| 설문조사 재검사     | post   | /with/mypage/survey/ |                         | 성공: 200, ok 실패: 400     |

