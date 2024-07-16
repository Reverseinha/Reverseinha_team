from rest_framework import serializers
from .models import *

class SignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True, label="비밀번호 확인")

    class Meta:
        model = MyUser
        fields = ['id', 'email', 'username', 'birth_date', 'gender', 'phone_number', 'password', 'password_confirm']
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
        return user


class LoginSerializer(serializers.Serializer):
    id = serializers.CharField(label="ID")
    password = serializers.CharField(write_only=True, label="비밀번호")

# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = '__all__'

# class CommentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comments
#         fields = ['author', 'content']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'username', 'birth_date', 'gender', 'phone_number', 'point']