from django.urls import path
from .views import signup, login_view, get_survey_questions, submit_survey_response, get_all_ads

urlpatterns = [
    path('', get_all_ads, name='get_all_ads'),  # 초기 화면 설정
    path('with/signup/', signup, name='signup'),
    path('with/login/', login_view, name='login'),
    path('survey/questions/', get_survey_questions, name='get_survey_questions'),
    path('survey/submit/', submit_survey_response, name='submit_survey_response'),
]