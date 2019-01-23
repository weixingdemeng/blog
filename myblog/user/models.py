from django.db import models


class User(models.Model):
    u_name = models.CharField(max_length=10, verbose_name='姓名')
    u_password = models.CharField(max_length=150, verbose_name='密码')
    # u_email = models.EmailField(verbose_name='邮箱')

    class Meta:
        db_table = 'user'