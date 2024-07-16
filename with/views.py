from django.shortcuts import render
from django.http import HttpResponseForbidden
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

@swagger_auto_schema(
    method="post",
    tags=["회원가입"],
    operation_summary="회원가입",
    operation_description="회원가입을 처리합니다.",
    request_body=SignUpSerializer,
    responses={
        201: '회원가입 성공',
        400: '잘못된 요청',
        500: '서버 오류'
    }
)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }, status=201)
    return Response(serializer.errors, status=400)


# 로그인
@swagger_auto_schema(
    method="post",
    tags=["로그인"],
    operation_summary="로그인",
    operation_description="로그인을 처리합니다.",
    request_body=LoginSerializer,
    responses={
        200: '로그인 성공',
        400: '잘못된 요청',
        500: '서버 오류'
    }
)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        id = serializer.validated_data.get('id')
        password = serializer.validated_data.get('password')
        user = authenticate(request, id=id, password=password) 
        if user is not None:
            user.last_login = timezone.now()  # 마지막 로그인 시간 갱신
            user.save()
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }, status=status.HTTP_200_OK)  # 로그인 성공 메시지 반환
        else:
            return Response({"error": "Invalid credentials"}, status=402)  # 오류 확인위해 추가
    return Response({"error": "Invalid credentials"}, status=400)
