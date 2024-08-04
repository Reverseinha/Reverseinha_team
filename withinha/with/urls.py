from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),  # 회원가입
    path('login/', login_view, name='login'),  # 로그인
    path('logout/', logout_view, name='logout'),  # 로그아웃
    path('user/id/', get_user_id, name='get_user_id'),  # 사용자 ID 조회
    path('user/nickname/', get_user_nickname, name='get_user_nickname'),  # 사용자 닉네임 조회
    path('signup/survey/', survey, name='survey'),  # 설문조사 URL 경로
    path('community/', CreatePostView.as_view(), name='create_post'),  # 게시물 작성
    path('community/search/', search_posts, name='search_posts'),  # 제목 검색
    path('community/all/', get_all_posts, name='get_all_posts'),  # 전체 게시물 조회
    path('community/<int:pk>/', get_post, name='get_post'),  # 특정 게시물 조회
    path('community/<int:pk>/update/', update_post, name='update_post'),  # 게시물 수정
    path('community/<int:pk>/delete/', delete_post, name='delete_post'),  # 게시물 삭제
    path('community/<int:post_pk>/comment/', create_comment, name='create_comment'),  # 댓글 작성
    path('community/<int:post_pk>/comments/all/', get_all_comments, name='get_all_comments'),  # 댓글 가져오기
    path('community/<int:post_pk>/comments/<int:pk>/delete/', delete_comment, name='delete_comment'),  # 댓글 삭제
    path('community/<int:post_pk>/comments/<int:pk>/update/', update_comment, name='update_comment'),  # 댓글 수정
    path('community/<int:post_pk>/toggle_like/', toggle_like, name='toggle_like'),  # 좋아요 토글

    # 날짜별 목표 및 일기 처리
    path('calendar/goal_diary/', GoalDiaryViewSet.as_view({'get': 'list'}), name='goal_diary_list'),  # 목표 및 일기 조회
    path('calendar/goal_diary/create/', GoalDiaryViewSet.as_view({'post': 'create_goal_diary'}), name='create_goal_diary'),  # 목표 및 일기 생성
    path('calendar/goal_diary/update/', GoalDiaryViewSet.as_view({'post': 'update_goal_diary'}), name='update_goal_diary'), # 목표 및 일기 수정
    path('consulting/', CounselingRequestViewSet.as_view({'post': 'create'}), name='consulting'),  # 상담 작성하기 URL 경로
    path('mypage/', MyPageView.as_view(), name='mypage'),  # 마이페이지 URL
]
