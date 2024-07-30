from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'goal_diary', GoalDiaryViewSet, basename='goal_diary')

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),  # 회원가입
    path('login/', login_view, name='login'),  # 로그인
    path('logout/', logout_view, name='logout'),  # 로그아웃
    path('signup/survey/', survey, name='survey'),  # 설문조사 URL 경로
    path('community/', CreatePostView.as_view(), name='create_post'), #게시물 작성
    path('community/search/', search_posts, name='search_posts'),  # 제목 검색
    path('community/all/', get_all_posts, name='get_all_posts'),  # 전체 게시물 조회
    path('community/<int:pk>/', get_post, name='get_post'),  # 특정 게시물 조회
    path('community/<int:post_pk>/comment/', create_comment, name='create_comment'),  # 댓글 작성
    path('community/<int:post_pk>/comments/all/', get_all_comments, name='get_all_comments'),  # 댓글 가져오기
    path('community/<int:post_pk>/comments/<int:pk>/delete/', delete_comment, name='delete_comment'),  # 댓글 삭제
    path('community/<int:post_pk>/comments/<int:pk>/update/', update_comment, name='update_comment'),  # 댓글 수정
    path('callendar/', include(router.urls)),  # 라우터를 URL 패턴에 포함
]
