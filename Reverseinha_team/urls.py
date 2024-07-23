from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('with/', include('with.urls')),
    path('with/', include('allauth.urls')),
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# /with/signup/: 회원가입 페이지
# /with/login/: 로그인 페이지
# /with/logout/: 로그아웃 페이지
# /with/confirm-email/: 이메일 인증 페이지
# /with/password/change/: 비밀번호 변경 페이지
# /with/password/reset/: 비밀번호 재설정 페이지
# /with/password/reset/done/: 비밀번호 재설정 완료 페이지
# /with/password/reset/key/: 비밀번호 재설정 키 페이지
# /with/password/reset/key/done/: 비밀번호 재설정 키 완료 페이지