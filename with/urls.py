from django.urls import path
from .views import signup, login_view, get_survey_questions, submit_survey_response

urlpatterns = [
    path('home/signup/', signup, name='signup'), # 회원가입
    path('home/login/', login_view, name='login'), # 로그인
    path('home/signup/survey/questons/',get_survey_questions, name='get_survey_questions'), # 설문조사 질문
    path('home/signup/survey/submit/', submit_survey_response, name='submit_survey_response'), # 설문조사 제출
]