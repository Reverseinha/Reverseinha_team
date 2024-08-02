from rest_framework import serializers
from .models import SurveyResponse, MyUser, Post, Comment, Day, Goal, DiaryEntry
from .models import CounselingRequest
from datetime import date

class SignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True, label="비밀번호 확인")

    class Meta:
        model = MyUser
        fields = ['id', 'email', 'username', 'nickname', 'birth_date', 'gender', 'phone_number', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "비밀번호가 일치하지 않습니다. 알맞게 입력해주세요."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = MyUser.objects.create_user(**validated_data)
        # 기본 SurveyResponse 생성
        # SurveyResponse.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    id = serializers.CharField(label="ID")
    password = serializers.CharField(write_only=True, label="비밀번호")

class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = ['user', 'answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'answer6', 'answer7', 'answer8', 'answer9', 'answer10']

    def get_score(self, obj):
        return obj.calculate_score()
    
class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.ReadOnlyField()
    total_comments = serializers.ReadOnlyField()
    author_name = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'image', 'author_name', 'total_likes', 'total_comments']
        read_only_fields = ['created_at']

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at']
        read_only_fields = ['created_at']

class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = '__all__'

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['user', 'day', 'text', 'is_completed']

class DiaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryEntry
        fields = ['user', 'day', 'title', 'content']

class GoalDiarySerializer(serializers.Serializer):
    goal = GoalSerializer()
    diary_entry = DiaryEntrySerializer()
    
    def create(self, validated_data):
        goal_data = validated_data.pop('goal')
        diary_entry_data = validated_data.pop('diary_entry')
        
        goal = Goal.objects.create(**goal_data)
        diary_entry = DiaryEntry.objects.create(**diary_entry_data)
        
        return {'goal': goal, 'diary_entry': diary_entry}
    
def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

class CounselingRequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    age = serializers.SerializerMethodField()

    class Meta:
        model = CounselingRequest
        fields = ['username', 'age', 'available_time', 'reason']

    def get_age(self, obj):
        return calculate_age(obj.user.birth_date)