from django.contrib import admin
from .models import *
from .serializers import *


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'birth_date', 'gender', 'phone_number', 'is_staff', 'last_login')
    search_fields = ('id', 'email', 'username', 'phone_number')
    readonly_fields = ('password',)  # 비밀번호를 읽기 전용으로 표시

    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        ('Personal info', {'fields': ('username', 'birth_date', 'gender', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
admin.site.register(SurveyQuestion)
admin.site.register(SurveyResponse)
admin.site.register(Slide)
admin.site.register(Post)
admin.site.register(Comment)