from django.urls import path
from .views import signup, login_view, get_survey_questions, submit_survey_response, create_post, search_posts, get_post, create_comment, get_all_comments, delete_comment, update_comment

urlpatterns = [
    path('home/signup/', signup, name='signup'), # 회원가입
    path('home/login/', login_view, name='login'), # 로그인
    path('home/signup/survey/questons/',get_survey_questions, name='get_survey_questions'), # 설문조사 질문
    path('home/signup/survey/submit/', submit_survey_response, name='submit_survey_response'), # 설문조사 제출
    path('home/community/', create_post, name='create_post'),  # 게시글 작성
    path('home/community/search/', search_posts, name='search_posts'),  # 제목 검색
    path('home/community/<int:pk>/', get_post, name='get_post'),  # 특정 게시물 조회
    path('home/community/<int:ad_id>/comment/', create_comment, name='create_comment'),  # 댓글 작성
    path('home/community/<int:ad_id>/comments/all/', get_all_comments, name='get_all_comments'), # 댓글 가져오기
    path('home/community/<int:ad_id>/comments/<int:pk>/delete/', delete_comment, name='delete_comment'),  # 댓글 삭제
    path('home/community/<int:ad_id>/comments/<int:pk>/update/', update_comment, name='update_comment'),  # 댓글 수정
]