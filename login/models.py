from django.db import models


class Admin(models.Model):
    """管理员"""
    user_name = models.CharField(verbose_name="用户名", max_length=32, unique=True, blank=False, null=False)
    password = models.CharField(verbose_name="密码", max_length=128, blank=False, null=False)

    def __str__(self):
        return self.user_name

# class NormalUser(models.Model):
#     """普通用户"""
#     nickname = models.CharField(verbose_name="昵称", max_length=32)
#     password = models.CharField(verbose_name="密码", max_length=64)
#     uid = models
