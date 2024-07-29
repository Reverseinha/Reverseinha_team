from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class MyUserManager(BaseUserManager):
    def create_user(self, id, email, username, birth_date, gender, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            id=id,
            email=email,
            username=username,
            birth_date=birth_date,
            gender=gender,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, email, username, birth_date, gender, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(id, email, username, birth_date, gender, phone_number, password, **extra_fields)

class MyUser(AbstractBaseUser, PermissionsMixin):
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
