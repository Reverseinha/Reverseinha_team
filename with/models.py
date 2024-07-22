from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User

class MyUserManager(BaseUserManager):
    def create_user(self, id, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(id=id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(id, email, password, **extra_fields)

class MyUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', '남자'),
        ('F', '여자'),
    ]
    
    id = models.CharField(max_length=10, unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)  # 사용자 이름
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='myuser_set',  # related_name 추가
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='myuser_set',  # related_name 추가
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email', 'username', 'birth_date', 'gender', 'phone_number']

    def __str__(self):
        return self.id

class SurveyQuestion(models.Model):
    question_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

class SurveyResponse(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    answer = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.id} - {self.question.id}"
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='ads/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        # 이 게시물의 좋아요 수를 반환합니다
        return self.likes.count()

    @property
    def total_proposals(self):
        # 이 게시물의 댓글 수를 반환합니다
        return self.proposals.count()

class Proposal(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='proposals')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'