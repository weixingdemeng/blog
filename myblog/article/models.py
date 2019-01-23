from django.db import models


class Article(models.Model):

    a_title = models.CharField(max_length=20)
    a_content = models.CharField(max_length=1500)
    a_pre = models.CharField(max_length=20)
    a_time = models.DateField(auto_now_add=True)
    a_category = models.IntegerField()

    class Meta:
        db_table = 'article'


class Category(models.Model):
    c_name = models.CharField(max_length=20)
    c_pre = models.CharField(max_length=20)

    class Meta:
        db_table = 'category'


class Bei(models.Model):
    b_name = models.CharField(max_length=20)
    b_pre = models.CharField(max_length=20)
    b_b = models.IntegerField()

    class Meta:
        db_table = 'bei'