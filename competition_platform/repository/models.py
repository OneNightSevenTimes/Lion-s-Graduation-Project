from django.db import models
from django.contrib.auth.models import  User
# Create your models here.

class UserProfile(models.Model):
    '''
    用户信息
    '''
    username = models.OneToOneField(User)
    password = models.CharField(max_length=32,blank=True,null=True)

    class Meta:
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.name

