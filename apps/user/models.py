from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager as _UserManager
# Create your models here.

# 方法重写
class UserManager(_UserManager):
    def create_superuser(self, username,  password,email=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        #
        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError('Superuser must have is_staff=True.')
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError('Superuser must have is_superuser=True.')
        # return self._create_user(username, email, password, **extra_fields)
    # 调用super方法
        super().create_superuser(username=username,password=password,email=email,**extra_fields)

class Users(AbstractUser):

    objects =  UserManager()

    REQUIRED_FIELDS = ['mobile']
    mobile = models.CharField(max_length=11, unique=True,verbose_name='手机号',help_text='手机号',error_messages={'unique':'此手机号已注册'})
    email_ac = models.BooleanField(default=False, verbose_name='邮箱状态')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'

    def __str__(self):
        return self.username

