
# 멋쟁이사자처럼 대학 12th HACKATHON
멋쟁이사자처럼 대학 12th HACKATHON에서 사용한 서버코드입니다. Django를 사용하여 구현하였습니다.


## 👨‍🏫 프로젝트 소개
**WITH**는 고립된 청년 및 자립준비 청년을 위한 종합 건강 지원 플랫폼 서비스로,  청년들이 직면한 정신적, 신체적 건강 문제 및 청년들의 맞춤형 건강 지원을 제공할 수 있게 도와주는 서비스입니다.

## ⏲️ 개발 기간
* 2024.07.14(일) ~ 2024.08.06(화)
    * 아이디어 제시
    * 와이어프레임 작성
    * 프론트와 협업


## 🧑‍🤝‍🧑 개발자 소개
* 염종섭
* 최우진


## ⚙️ 기술 스택
* Server: AWS EC2
* WS/WAS: Nginx
* 아이디어 회의: Notion
* [Notion 링크](https://www.notion.so/5c39c682496f45569c76f5d9950a82c8)


## ✒️ API

### 사용자 인증관리
| 기능         | method | REST API              |
|--------------|--------|-----------------------|
| 회원가입     | post   | /with/signup/         |
| 로그인       | post   | /with/login/          |
| 로그아웃     | post   | /with/logout/         |
| 설문조사 제출 | post   | /with/signup/survey/  |

### 커뮤니티
| 기능                 | method | REST API                                             |
|----------------------|--------|------------------------------------------------------|
| 게시글 생성          | post   | /with/community/                                     |
| 게시글 제목검색      | get    | /with/community/search/                              |
| 특정 게시글 조회     | get    | /with/community/int:<int:pk>/                        |
| 전체 게시글 조회     | get    | /with/community/all/                                 |
| 댓글 작성            | post   | /with/community/int:<int:post_pk>/comment/           |
| 댓글 가져오기        | get    | /with/community/int:<int:post_pk>/comments/all/      |
| 댓글 삭제            | delete | /with/community/int:<int:post_pk>/comments/int:<int:pk>/delete/ |
| 댓글 수정            | put    | /with/community/int:<int:post_pk>/comments/int:<int:pk>/update/ |

### 사용자 정보
| 기능                  | method | REST API                  |
|-----------------------|--------|---------------------------|
| 사용자 ID 조회        | get    | /with/user/id/            |
| 사용자 닉네임 조회    | get    | /with/user/nickname/      |

### 캘린더
| 기능                       | method | REST API                                      |
|----------------------------|--------|-----------------------------------------------|
| 목표 및 일기 조회          | get    | /with/calendar/goal_diary/?date=날짜          |
| 목표 생성                  | post   | /with/calendar/goal/create/                   |
| 목표 삭제                  | delete | /with/calendar/goal/int:<int:pk>/delete/      |
| 목표 완료 상태 업데이트    | patch  | /with/calendar/goal/int:<int:pk>/completed/   |
| 일기 생성                  | post   | /with/calendar/diary/create/                  |
| 일기 수정                  | post   | /with/calendar/diary/update/                  |
| 일기 삭제                  | delete | /with/calendar/diary/int:<int:pk>/delete/     |

### 상담신청
| 기능                | method | REST API           |
|---------------------|--------|--------------------|
| 상담 작성하기       | post   | /with/consulting/application/  |

### 마이페이지
| 기능                | method | REST API           |
|---------------------|--------|--------------------|
| 마이페이지           | get    | /with/mypage/      |
| 설문조사 재검사     | post   | /with/mypage/survey/ |
