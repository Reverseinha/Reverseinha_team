from pathlib import Path
import os
from datetime import timedelta
from django.urls import reverse_lazy


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm)xg6+9es(t75ilvij$$(ww_@y!ene*=sf4yr@1qh4kza2+-n*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

#Auth 세팅
AUTH_USER_MODEL = 'with.MyUser'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'with', # 추가
    "rest_framework",
    'rest_framework_simplejwt', #추가
    "drf_yasg",
    'corsheaders',
     #allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',


    #provider
    # 페이스북 등 추가하고싶은 것이 있다면 여기에 추가하면 됨.
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.kakao',

]
LOGIN_REDIRECT_URL = 'home/'  # 로그인 후 리다이렉트 될 경로
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     # 추가할 미들웨어
    'allauth.account.middleware.AccountMiddleware',
]
# CORS 설정 추가
CORS_ALLOW_ALL_ORIGINS = True  # 모든 도메인에서의 요청을 허용
CORS_ALLOW_CREDENTIALS = True


SITE_ID = 1

LOGIN_REDIRECT_URL = '/'  # 로그인 후 리다이렉트 될 경로
ACCOUNT_LOGOUT_REDIRECT_URL = reverse_lazy('accountapp:login')
ACCOUNT_LOGOUT_ON_GET = True

ROOT_URLCONF = 'Reverseinha_team.urls'
# 또는 특정 도메인만 허용하려면 아래 설정을 사용
CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:3000',
    'http://localhost:8000',
]
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

REST_USE_JWT = True


SIMPLE_JWT = {
    'SIGNING_KEY': 'hellolikelionhellolikelion',
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}


WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    # Django 관리자 페이지에서 사용자 이름으로 로그인할 수 있도록 필요
    "django.contrib.auth.backends.ModelBackend",
    # 이메일로 로그인과 같은 `allauth` 전용 인증 방법
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr' # 언어를 한국어로 변경해줍니다

TIME_ZONE = 'Asia/Seoul' # 시간대를 서울로 변경해줍니다

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')