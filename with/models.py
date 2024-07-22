from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_migrate


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
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return self.title

# class Site(models.Model):
#     SITE_CHOICES = [
#         ('intern', '해외취업'),
#         ('language-study', '어학연수'),
#         ('working-holiday', '워킹홀리데이'),
#     ]
#     site_name = models.CharField(max_length=15, choices=SITE_CHOICES, unique=True)
    
#     def __str__(self):
#         return self.get_site_name_display()


# class Category(models.Model):
#     CATEGORY_CHOICES = [
#         ('community', '커뮤니티'),
#         ('group-buying', '공구'),
#         ('agency-document', '대행, 서류작성'),
#         ('info', '정보'),
#     ]
#     category_name = models.CharField(max_length=15, choices=CATEGORY_CHOICES, unique=True)

#     def __str__(self):
#         return self.get_category_name_display()

# class SiteCategory(models.Model):
#     site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

# class Post(models.Model):
#     country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
#     continent = models.ForeignKey(Continent, on_delete=models.SET_NULL, null=True)
#     author = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
#     site_category = models.ForeignKey(SiteCategory, on_delete=models.SET_NULL, null=True)
#     site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     images = models.ImageField(upload_to='images/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     likes = models.IntegerField(default=0)

#     def __str__(self):
#         return self.title


# class Comments(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
#     author = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
#     content = models.CharField(max_length=100)
#     create_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.content