from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator

class User(AbstractBaseUser, PermissionsMixin):
    """
    用户基本信息表（不包含任何认证凭据）
    """
    phone_validator = RegexValidator(regex=r'^1[3-9]\d{9}$', message='手机号格式错误')

    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[phone_validator],
        verbose_name='手机号'
    )
    username = models.CharField(max_length=150, blank=True, null=True, verbose_name='昵称')
    avatar_url = models.URLField(blank=True, null=True, verbose_name='头像URL')
    user_type = models.CharField(
        max_length=20,
        choices=[('player', '普通用户'), ('inheritor', '管理员'), ('other', '其他')],
        default='other',
        verbose_name='用户类型'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # 告诉 Django 用 phone 字段作为登录标识
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []   # 不需要额外必填字段

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.phone


class CredentialType(models.TextChoices):
    PASSWORD = 'password', '密码'
    WECHAT = 'wechat', '微信'
    EMAIL = 'email', '邮箱'


class Credential(models.Model):
    """
    用户凭据表：一个用户可以有多种登录方式
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credentials')
    credential_type = models.CharField(max_length=20, choices=CredentialType.choices)
    identifier = models.CharField(max_length=255, db_index=True)
    credential = models.CharField(max_length=255)                  # 密码哈希、token等
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'credentials'
        unique_together = [['credential_type', 'identifier']]
        indexes = [
            models.Index(fields=['credential_type', 'identifier']),
        ]

    def __str__(self):
        return f"{self.user.phone} - {self.credential_type}"