from django.db import models


class Share(models.Model):
    objects = models.Manager()

    url = models.URLField()
    password = models.CharField(max_length=50, null=True)
    readCountLimit = models.IntegerField(null=True)
    expiredAt = models.DateTimeField(null=True)


class Tag(models.Model):
    objects = models.Manager()

    guid = models.UUIDField(primary_key=True, verbose_name='tagGuid')
    name = models.CharField(max_length=200, verbose_name='标签名称')
    version = models.IntegerField(verbose_name='版本号')


class Doc(models.Model):
    objects = models.Manager()

    guid = models.UUIDField(primary_key=True, verbose_name='docGuid')
    created = models.DateTimeField(verbose_name='创建时间')

    version = models.IntegerField(verbose_name='版本号')

    category = models.CharField(max_length=200, verbose_name='文件夹名称')
    title = models.CharField(max_length=200, verbose_name='文章标题')
    text = models.TextField(null=True, verbose_name='html格式正文')

    tags = models.ManyToManyField(to=Tag)

    share = models.ForeignKey(to=Share, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-created']
