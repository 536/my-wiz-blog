import logging
from datetime import datetime
from html import unescape

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
        wiz_docs = [_ for _ in docs if _['title'].endswith('.md')]
        wiz_docs_guid = [_['docGuid'] for _ in docs if _['title'].endswith('.md')]

        for doc in self.filter(category=category):
            if doc.guid in wiz_docs_guid:
                wiz_doc = [_ for _ in wiz_docs if _['docGuid'] == doc.guid][0]
                if doc.version_id != wiz_doc['version']:
                    text = wiz.get_note_view(docGuid=wiz_doc['docGuid']).text
                    tags = wiz_doc.get('tags')
                    if tags:
                        tags = tags.split('*')
                        Tag.objects.filter(guid__in=tags).update(using=True)
                        version = DocVersion.objects.add(
                            version=wiz_doc['version'],
                            title=wiz_doc['title'],
                            text=text,
                            tags=tags
                        )
                        doc.update(version=version)
                wiz_docs_guid.remove(doc.guid)
            else:
                doc.delete()

        for wiz_doc_guid in wiz_docs_guid:
            wiz_doc = [_ for _ in wiz_docs if _['docGuid'] == wiz_doc_guid]
            if wiz_doc:
                wiz_doc = wiz_doc[0]

                logger.info(wiz_doc)
                text = unescape(wiz.get_note_view(docGuid=wiz_doc['docGuid']).text)
                tags = wiz_doc.get('tags')
                tags = tags.split('*') if tags else []
                Tag.objects.filter(guid__in=tags).update(using=True)
                version = DocVersion.objects.add(
                    version=wiz_doc['version'],
                    title=wiz_doc['title'],
                    text=text,
                    tags=tags
                )
                Doc.objects.create(
                    guid=wiz_doc['docGuid'],
                    created=datetime.fromtimestamp(wiz_doc['created'] / 1000, tz=get_current_timezone()),
                    category=category,
                    version=version,
                )


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
