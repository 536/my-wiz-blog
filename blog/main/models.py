from django.db import models


class Category(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=200, verbose_name='文件夹名称')


class Doc(models.Model):
    objects = models.Manager()

    guid = models.UUIDField(primary_key=True, verbose_name='docGuid')
    title = models.CharField(max_length=200, verbose_name='文章标题')
    version = models.IntegerField(verbose_name='版本号')
    readCount = models.IntegerField(verbose_name='阅读次数')
    created = models.DateTimeField(verbose_name='创建时间')
    accessed = models.DateTimeField(verbose_name='访问时间')

    text = models.TextField(null=True, verbose_name='html格式原文')
    md = models.TextField(null=True, verbose_name='md格式正文')
    html = models.TextField(null=True, verbose_name='html格式正文')

    Category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
