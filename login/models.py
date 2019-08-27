from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class User(models.Model):
    """用户表"""
    gender = (
        ('male', '男'),
        ('female', '女'),
        ('secret','保密'),
    )

    name = models.CharField(verbose_name='用户名', max_length=128, unique=True)
    password = models.CharField(verbose_name='密码', max_length=256)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    sex = models.CharField(verbose_name='性别', max_length=32, choices=gender, default='保密')
    c_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = "用户名"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name