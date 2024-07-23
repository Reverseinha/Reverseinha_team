from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Count, Q
from datetime import datetime
import json

from .models import Goal, DiaryEntry, Post, Comment, SurveyQuestion, SurveyResponse, Day, Slide
from .serializers import GoalSerializer, DiaryEntrySerializer, PostSerializer, CommentSerializer, SignUpSerializer, LoginSerializer, SurveyQuestionSerializer, SurveyResponseSerializer


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


@login_required
@api_view(['GET'])
def get_user_survey_responses(request):
    user = request.user
    responses = SurveyResponse.objects.filter(user=user)
    serializer = SurveyResponseSerializer(responses, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    data = request.data
    title = data.get('title')
    content = data.get('content')
    image = request.FILES.get('image')

    post = Post(
        title=title,
        content=content,
        image=image,
        author=request.user  # 게시글 작성자 설정
    )
    post.save()
    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    serializer = PostSerializer(post)
    return Response(serializer.data, status=200)


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
@permission_classes([IsAuthenticated])
def create_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(post=post, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_comments(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comments = post.comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, post_id=post_pk, pk=comment_pk)
    if request.user != comment.author:
        return Response({'error': 'You can only edit your own comments.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, post_id=post_pk, pk=comment_pk)
    if request.user != comment.author:
        return Response({'error': 'You can only delete your own comments.'}, status=status.HTTP_403_FORBIDDEN)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def home(request):
    slides = Slide.objects.all()
    return render(request, {'slides': slides})


class GoalDiaryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({"detail": "Date parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        goals = Goal.objects.filter(user=user, day__date=date)
        diary_entries = DiaryEntry.objects.filter(user=user, day__date=date)

        goals_serializer = GoalSerializer(goals, many=True)
        diary_entries_serializer = DiaryEntrySerializer(diary_entries, many=True)

        return Response({
            'goals': goals_serializer.data,
            'diary_entries': diary_entries_serializer.data
        })

    @action(detail=False, methods=['post'])
    def create_goal(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = GoalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_diary_entry(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = DiaryEntrySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_diary_entry(self, request, pk=None):
        diary_entry = DiaryEntry.objects.get(pk=pk, user=request.user)
        serializer = DiaryEntrySerializer(diary_entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_diary_entry(self, request, pk=None):
        diary_entry = DiaryEntry.objects.get(pk=pk, user=request.user)
        diary_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)