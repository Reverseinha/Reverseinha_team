from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import signup, login_view, get_survey_questions, submit_survey_response, create_post, search_posts, get_post, create_comment, get_all_comments, delete_comment, update_comment, home, get_user_survey_responses, GoalDiaryViewSet

router = DefaultRouter()
router.register(r'goal_diary', GoalDiaryViewSet, basename='goal_diary')

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),  # 회원가입
    path('login/', login_view, name='login'),  # 로그인
    path('survey/questions/', get_survey_questions, name='get_survey_questions'),  # 설문조사 질문
    path('survey/submit/', submit_survey_response, name='submit_survey_response'),  # 설문조사 제출
    path('community/', create_post, name='create_post'),  # 게시글 작성
    path('community/search/', search_posts, name='search_posts'),  # 제목 검색
    path('community/<int:pk>/', get_post, name='get_post'),  # 특정 게시물 조회
    path('community/<int:ad_id>/comment/', create_comment, name='create_comment'),  # 댓글 작성
    path('community/<int:ad_id>/comments/all/', get_all_comments, name='get_all_comments'),  # 댓글 가져오기
    path('community/<int:ad_id>/comments/<int:pk>/delete/', delete_comment, name='delete_comment'),  # 댓글 삭제
    path('community/<int:ad_id>/comments/<int:pk>/update/', update_comment, name='update_comment'),  # 댓글 수정
    path('user/survey_responses/', get_user_survey_responses, name='get_user_survey_responses'),  # 사용자 설문조사 데이터 조회
    path('callendar/', include(router.urls)),  # 라우터를 URL 패턴에 포함
]

# path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
# path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

# # Swagger url
# re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
# re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),