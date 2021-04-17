import logging
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.utils.timezone import get_current_timezone

from .utils import wiz_html_to_md, markdown
from system.models import System

logger = logging.getLogger('django')


class VersionManager(models.Manager):
    def add(self, version: int, title: str, text: str, tags: list):
        md = '\n'.join(list(wiz_html_to_md(text)))
        html = markdown(md)
        version = self.model(
            version=version,
            title=title,
            text=text,
            md=md,
            html=html
        )
        version.save()
        version.tags.add(*tags)
        return version


class TagManager(models.Manager):
    def periodical_update(self, tags):
        wiz_tags = [tag['tagGuid'] for tag in tags]

        for tag in self.all():
            if tag.guid not in wiz_tags:
                tag.delete()
            else:
                wiz_tag = [_ for _ in tags if _['tagGuid'] == tag.guid][0]
                if tag.version != wiz_tag['version']:
                    tag.update(name=wiz_tag['name'], parent=wiz_tag['parentTagGuid'], version=wiz_tag['version'])
                wiz_tags.remove(tag.guid)

        self.bulk_create([
            self.model(guid=_['tagGuid'], name=_['name'], version=_['version'])
            for _ in tags
        ])


class CategoryManager(models.Manager):
    def periodical_update(self, categories):
        wiz_categories = [_ for _ in categories if _.startswith(System.objects.get_key('CATEGORY'))]

        for category in self.all():
            if category.name not in wiz_categories:
                category.delete()
            else:
                wiz_categories.remove(category.name)

        self.bulk_create([
            self.model(name=_)
            for _ in wiz_categories
        ])


class DocManager(models.Manager):
    def periodical_update(self, wiz, docs, category):
        # 远端数据
        wiz_docs = [_ for _ in docs if _['title'].endswith('.md')]
        wiz_docs_guid = [_['docGuid'] for _ in docs if _['title'].endswith('.md')]

        for doc in self.filter(category=category):
            # 已保存的远端数据
            if doc.guid in wiz_docs_guid:
                for wiz_doc in wiz_docs:
                    if wiz_doc['docGuid'] == doc.guid:
                        # 版本号一致
                        if doc.version_id == wiz_doc['version']:
                            wiz_docs_guid.remove(doc.guid)
                        break
            # 远端不存在的数据 / 远端存在但是本地版本号不一致
            # 删除本地数据 / 删除本地数据再新增
            doc.delete()

        # 远端存在但是本地没有的数据 / 远端存在但是本地版本号不一致的数据
        # 新增
        for wiz_doc_guid in wiz_docs_guid:
            for wiz_doc in wiz_docs:
                if wiz_doc['docGuid'] == wiz_doc_guid:
                    note = wiz.download_note(docGuid=wiz_doc_guid, downloadInfo=1, downloadData=1).json()
                    text = note['html']
                    tags = wiz_doc.get('tags').split('*') if wiz_doc.get('tags') else []
                    Tag.objects.filter(guid__in=tags).update(using=True)
                    version = DocVersion.objects.add(
                        version=wiz_doc['version'],
                        title=wiz_doc['title'],
                        text=text,
                        tags=tags
                    )
                    doc = Doc.objects.create(
                        guid=wiz_doc_guid,
                        created=datetime.fromtimestamp(wiz_doc['created'] / 1000, tz=get_current_timezone()),
                        category=category,
                        version=version,
                    )
                    resources = note.get('resources') if note.get('resources') else []
                    for resource in resources:
                        res, created = Resource.objects.get_or_create(name=resource['name'], doc=doc, version=version)
                        if created:
                            res.file.save(resource['name'], ContentFile(wiz.session.get(resource['url']).content))

                            version.html = version.html.replace(
                                'index_files/%s' % res.name,
                                '%s%s/%s/index_files/%s' % (
                                    settings.MEDIA_URL,
                                    doc.guid,
                                    version.version,
                                    res.name
                                )
                            )
                            version.save()
                    break


class Tag(models.Model):
    objects = TagManager()

    guid = models.UUIDField(primary_key=True, verbose_name='tagGuid')
    parent = models.UUIDField(null=True, verbose_name='parentTagGuid')
    name = models.CharField(max_length=200, verbose_name='标签名称')
    version = models.IntegerField(verbose_name='版本号')
    using = models.BooleanField(default=False, verbose_name='是否与doc相关联')


class Category(models.Model):
    objects = CategoryManager()

    name = models.CharField(max_length=200, verbose_name='文件夹名称')


class DocVersion(models.Model):
    objects = VersionManager()

    version = models.IntegerField(primary_key=True, verbose_name='版本号')
    title = models.CharField(max_length=200, verbose_name='文章标题')
    text = models.TextField(null=True, verbose_name='html格式原文')
    md = models.TextField(null=True, verbose_name='md格式正文')
    html = models.TextField(null=True, verbose_name='html格式正文')

    tags = models.ManyToManyField(to=Tag)


class Doc(models.Model):
    objects = DocManager()

    guid = models.UUIDField(primary_key=True, verbose_name='docGuid')
    created = models.DateTimeField(verbose_name='创建时间')

    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    version = models.ForeignKey(to=DocVersion, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']


def resource_upload_to(instance, filename):
    return Path(settings.MEDIA_ROOT) / instance.doc_id / str(instance.version.version) / 'index_files' / filename


class Resource(models.Model):
    objects = models.Manager()

    file = models.FileField(upload_to=resource_upload_to)
    name = models.CharField(max_length=200)

    doc = models.ForeignKey(to=Doc, on_delete=models.CASCADE)
    version = models.ForeignKey(to=DocVersion, on_delete=models.CASCADE)
