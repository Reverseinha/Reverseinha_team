from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, SurveyResponse, Post, Comment, Slide, Goal, DiaryEntry, Day

class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('id', 'email', 'username', 'nickname', 'birth_date', 'gender', 'phone_number', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'gender')
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        ('Personal Info', {'fields': ('username', 'nickname', 'birth_date', 'gender', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'email', 'username', 'nickname', 'birth_date', 'gender', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('id', 'email', 'username', 'nickname')
    ordering = ('id',)


class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'answer6', 'answer7', 'answer8', 'answer9', 'answer10')
    list_filter = ('answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'answer6', 'answer7', 'answer8', 'answer9', 'answer10')
    search_fields = ('user__id',)

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(SurveyResponse, SurveyResponseAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Slide)
admin.site.register(Goal)
admin.site.register(DiaryEntry)
admin.site.register(Day)
