from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
import uuid

class ChoreTrackerUserManager(BaseUserManager):
    def create_user(self, email, username, password, is_managed, **extra_fields):
        
        if is_managed: # 被管理ユーザーはユーザー名で登録
            if not username:
                raise ValueError('The Username field must be set')
            # ユーザー名に@が含まれていたらエラー
            if '@' in username:
                raise ValueError('The Username field must not contain @')
            
            # メールアドレスは削除
            email = None

        else: # 一般ユーザーはメールアドレスで登録
            if not email:
                raise ValueError('The Email field must be set')
            # ユーザー名は削除
            username = None

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, is_managed=is_managed, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_managed', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_managed') is not False:
            raise ValueError('Superuser must have is_managed=False.')
        return self.create_user(**extra_fields)

class ChoreTrackerUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True, null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_managed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = ChoreTrackerUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        if self.is_managed:
            return self.username
        else:
            return self.email

# Create your models here.
