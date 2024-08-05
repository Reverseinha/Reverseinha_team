from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import login, authenticate, logout
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
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q, Count
from django.db import transaction
from .serializers import DiaryEntrySerializer
import json
import datetime
from .models import Goal, DiaryEntry, Post, Comment, SurveyResponse, Day, Slide
from .serializers import GoalSerializer, DiaryEntrySerializer, PostSerializer, CommentSerializer, SignUpSerializer, LoginSerializer, SurveyResponseSerializer, GoalDiarySerializer
from .models import CounselingRequest
from .serializers import CounselingRequestSerializer    
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
        with transaction.atomic():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
                'user_id': user.id,
                'message': '회원가입 성공. 이제 설문조사를 진행해주세요.',
                'redirect_url': '/signup/survey/'  # 설문조사 페이지 URL
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


@swagger_auto_schema(
    method="post",
    tags=["로그아웃"],
    operation_summary="로그아웃",
    operation_description="로그아웃을 처리합니다.",
    responses={
        200: '로그아웃 성공',
        400: '잘못된 요청',
        500: '서버 오류'
    }
)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({
        'message': '로그아웃 성공'
    }, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method="post",
    tags=["설문조사"],
    operation_summary="설문조사",
    operation_description="설문조사를 처리합니다.",
    request_body=SurveyResponseSerializer(many=True),
    responses={
        201: '설문조사 성공',
        400: '잘못된 요청',
        500: '서버 오류'
    }
)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def survey(request):
    user = request.user
    serializer = SurveyResponseSerializer(data=request.data)
    if serializer.is_valid():
        survey_response = serializer.save(user=user)
        response_data = serializer.data
        response_data['score'] = survey_response.calculate_score()
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        title = data.get('title')
        content = data.get('content')
        image = request.FILES.get('image')

        post = Post(
            title=title,
            content=content,
            image=image,
            user=request.user  # 게시글 작성자 설정
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
def get_all_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def search_posts(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'latest')

    # 유효한 정렬 기준 리스트
    valid_sort_options = ['latest', 'oldest', 'popular']

    # 디버깅용 출력
    print(f"Query: {query}, Sort by: {sort_by}")

    # 유효성 검사
    if sort_by not in valid_sort_options:
        return Response({'error': f"Invalid sort option: {sort_by}. Valid options are 'latest', 'oldest', and 'popular'."}, status=400)

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

    # 디버깅용 출력
    print(f"Posts after sorting: {posts.query}")

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=200)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.user:
        return Response({'error': 'You can only edit your own posts.'}, status=status.HTTP_403_FORBIDDEN)
    
    data = request.data
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    
    if 'image' in request.FILES:
        post.image = request.FILES['image']

    post.save()
    serializer = PostSerializer(post)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        message = "Like removed."
    else:
        post.likes.add(request.user)
        message = "Liked."
    return Response({'message': message, 'total_likes': post.total_likes}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.user:
        return Response({'error': 'You can only delete your own posts.'}, status=status.HTTP_403_FORBIDDEN)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

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
def update_comment(request, post_pk, pk):
    comment = get_object_or_404(Comment, post_id=post_pk, pk=pk)
    if request.user != comment.author:
        return Response({'error': 'You can only edit your own comments.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, post_pk, pk):
    comment = get_object_or_404(Comment, post_id=post_pk, pk=pk)
    if request.user != comment.author:
        return Response({'error': 'You can only delete your own comments.'}, status=status.HTTP_403_FORBIDDEN)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def home(request):
    slides = Slide.objects.all()
    return render(request, {'slides': slides})

class GoalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

    def perform_create(self, serializer):
        day_date_str = self.request.data.get('day')
        try:
            day_date = datetime.datetime.strptime(day_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        day, created = Day.objects.get_or_create(date=day_date)
        serializer.save(user=self.request.user, day=day)

    @action(detail=True, methods=['post'], url_path='completed')
    def mark_completed(self, request, pk=None):
        try:
            goal = self.get_object()
            is_completed = request.data.get('is_completed')

            if is_completed is not None:
                goal.is_completed = is_completed
                goal.save()
                return Response(GoalSerializer(goal).data)
            else:
                return Response({"detail": "is_completed field is required."}, status=status.HTTP_400_BAD_REQUEST)
        except Goal.DoesNotExist:
            return Response({"detail": "Goal not found."}, status=status.HTTP_404_NOT_FOUND)
    
class DiaryEntryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DiaryEntry.objects.all()
    serializer_class = DiaryEntrySerializer

    def perform_create(self, serializer):
        day_date_str = self.request.data.get('day')
        try:
            day_date = datetime.datetime.strptime(day_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        day, created = Day.objects.get_or_create(date=day_date)
        serializer.save(user=self.request.user, day=day)

    @action(detail=False, methods=['post'], url_path='update')
    def update_entry(self, request):
        day_date_str = request.data.get('day')
        try:
            day_date = datetime.datetime.strptime(day_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            diary_entry = DiaryEntry.objects.get(day__date=day_date, user=request.user)
        except DiaryEntry.DoesNotExist:
            return Response({"detail": "Diary entry not found."}, status=status.HTTP_404_NOT_FOUND)

        day, created = Day.objects.get_or_create(date=day_date)
        serializer = self.get_serializer(diary_entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=self.request.user, day=day)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete')
    def delete_entry(self, request):
        day_date_str = request.data.get('day')
        try:
            day_date = datetime.datetime.strptime(day_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            diary_entry = DiaryEntry.objects.get(day__date=day_date, user=request.user)
        except DiaryEntry.DoesNotExist:
            return Response({"detail": "Diary entry not found."}, status=status.HTTP_404_NOT_FOUND)

        diary_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GoalDiaryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({"detail": "Date parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
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

    
class CounselingRequestViewSet(viewsets.ModelViewSet):
    queryset = CounselingRequest.objects.all()
    serializer_class = CounselingRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 설문조사 점수 조회
        survey_response = SurveyResponse.objects.filter(user=user).first()
        survey_score = survey_response.calculate_score() if survey_response else 0

        # 일기 조회
        diary_entries = DiaryEntry.objects.filter(user=user)

        # 상담 신청 기록 조회
        counseling_requests = CounselingRequest.objects.filter(user=user)

        # 목표 조회 및 목표 달성 비율 계산
        goals = Goal.objects.filter(user=user)
        total_goals = goals.count()
        completed_goals = goals.filter(is_completed=True).count()
        goal_achievement_rate = (completed_goals / total_goals * 100) if total_goals > 0 else 0

        data = {
            "survey_score": survey_score,
            "diary_entries": DiaryEntrySerializer(diary_entries, many=True).data,
            "counseling_requests": CounselingRequestSerializer(counseling_requests, many=True).data,
            "goals": GoalSerializer(goals, many=True).data,
            "goal_achievement_rate": goal_achievement_rate
        }

        return Response(data, status=status.HTTP_200_OK)
    


@api_view(['GET'])
def get_user_id(request):
    user_id = request.user.id
    return Response({'id': user_id}, status=200)

@api_view(['GET'])
def get_user_nickname(request):
    nickname = request.user.nickname
    return Response({'nickname': nickname}, status=200)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_survey(request):
    user = request.user
    try:
        survey_response = SurveyResponse.objects.get(user=user)
        serializer = SurveyResponseSerializer(survey_response, data=request.data)
    except SurveyResponse.DoesNotExist:
        serializer = SurveyResponseSerializer(data=request.data)

    if serializer.is_valid():
        with transaction.atomic():
            survey_response = serializer.save(user=user)
            response_data = serializer.data
            response_data['score'] = survey_response.calculate_score()
            return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_survey(self, request):
        user = request.user

        # 설문조사 점수 조회
        survey_response = SurveyResponse.objects.filter(user=user).first()
        survey_score = survey_response.calculate_score() if survey_response else 0

        data = {
            "survey_score": survey_score
        }

        return Response(data, status=status.HTTP_200_OK)

@action(detail=True, methods=['delete'], url_path='delete')
def delete_goal(self, request, pk=None):
        try:
            goal = self.get_object()
            goal.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Goal.DoesNotExist:
            return Response({"detail": "Goal not found."}, status=status.HTTP_404_NOT_FOUND)
