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
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Post
from .serializers import PostSerializer
from django.db.models import Count, Q


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
@permission_classes[AllowAny]
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
            response = Response({
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }, status=status.HTTP_200_OK)  # 로그인 성공 메시지 반환
            response['Location'] = '/'  # 홈 화면으로 리디렉션
            return response
        else:
            return Response({"error": "Invalid credentials"}, status=402)  # 오류 확인위해 추가
    return Response({"error": "Invalid credentials"}, status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_survey_questions(request):
    questions = SurveyQuestion.objects.all()
    serializer = SurveyQuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_survey_response(request):
    serializer = SurveyResponseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_post(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('data'))  # form-data에서 데이터를 가져옵니다.
        
        title = data.get('title')
        content = data.get('content')
        image = request.FILES.get('image')  # 파일 데이터를 가져옵니다.

        post = Post(
            title=title,
            content=content,
    
            image=image
        )
        post.save()
        return Response({'message': 'success'})
    return Response({'message': 'POST 요청만 허용됩니다.'}, status=400)

# 특정 한 게시물 가져오기
@api_view(['GET'])
def get_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    serializer = PostSerializer(post)
    return Response(serializer.data, status=200)

# 검색어로 게시물 조회 (검색 기능)
@api_view(['GET'])
def search_posts(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'latest')

    posts = Post.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    if sort_by == 'latest':
        posts = posts.order_by('-created_at')
    elif sort_by == 'oldest':
        posts = posts.order_by('created_at')
    elif sort_by == 'popular':
        posts = posts.annotate(likes_count=Count('likes')).order_by('-likes_count')

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(post=post, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_comments(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comments = post.comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=200)

@api_view(['PUT'])
def edit_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, post_id=post_pk, pk=comment_pk)
    if request.user != comment.author:
        return Response({'error': 'You can only edit your own comments.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, post_id=post_pk, pk=comment_pk)
    if request.user != comment.author:
        return Response({'error': 'You can only delete your own comments.'}, status=status.HTTP_403_FORBIDDEN)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)