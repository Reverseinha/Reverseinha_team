from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),  # 회원가입
    path('login/', login_view, name='login'),  # 로그인
    path('logout/', logout_view, name='logout'),  # 로그아웃
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
    path('calendar/goal/create/', GoalViewSet.as_view({'post': 'create'}), name='create_goal'),  # 목표 생성
    path('calendar/goal/<int:pk>/completed/', GoalViewSet.as_view({'patch': 'mark_completed'}), name='mark_goal_completed'),  # 목표 완료 상태 업데이트
    path('calendar/diary/create/', DiaryEntryViewSet.as_view({'post': 'create'}), name='create_diary'),  # 일기 생성
    path('calendar/diary/update/', DiaryEntryViewSet.as_view({'post': 'update_entry'}), name='update_diary'),  # 일기 수정
    path('calendar/diary/delete/', DiaryEntryViewSet.as_view({'delete': 'delete_entry'}), name='delete_diary'),  # 일기 삭제
    path('consulting/', CounselingRequestViewSet.as_view({'post': 'create'}), name='consulting'),  # 상담 작성하기 URL 경로
    path('mypage/', MyPageView.as_view(), name='mypage'),  # 마이페이지 URL
    path('mypage/survey/', update_survey, name='update_survey'),  # 설문조사 업데이트 URL 경로

]
