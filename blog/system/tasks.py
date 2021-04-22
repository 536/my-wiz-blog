# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/4/5 21:41
# @Author  : https://github.com/536
from datetime import datetime

from bs4 import BeautifulSoup
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import get_current_timezone
from wiz import Wiz

from system.models import System
from wiznote.models import Tag, Doc, Share


@shared_task
def update_wiz():
    wiz_periodical_update()


def wiz_periodical_update():
    with Wiz(username=System.objects.get(key='WIZ_USERNAME').value,
             password=System.objects.get(key='WIZ_PASSWORD').value) as wiz:
        # tag
        for _ in wiz.get_tags().json()['result']:
            try:
                Tag.objects.get(
                    guid=_['tagGuid'],
                    version=_['version'],
                )
            except ObjectDoesNotExist:
                Tag.objects.create(
                    guid=_['tagGuid'],
                    name=_['name'],
                    version=_['version'],
                )

        # category
        root = System.objects.get_key('CATEGORY')
        categories = [
            _ for _ in wiz.get_category().json()['result']
            if root and _.startswith(root)
        ]

        for category in categories:
            docs = [
                _ for _ in wiz.get_notes_of_folder(
                    category=category,
                    withAbstract=False,
                    start=0,
                    count=50
                ).json()['result']
                if _['title'].endswith('.md')
            ]

            Doc.objects.exclude(guid__in=[_['docGuid'] for _ in docs]).delete()

            for _ in docs:
                try:
                    doc = Doc.objects.get(guid=_['docGuid'])
                except ObjectDoesNotExist:
                    doc = Doc.objects.create(
                        guid=_['docGuid'],
                        version=_['version'],
                        created=datetime.fromtimestamp(_['created'] / 1000, tz=get_current_timezone()),
                        category=_['category'],
                        title=_['title'],
                        text=BeautifulSoup(
                            wiz.get_note_view(_['docGuid']).content,
                            features='html.parser'
                        ).body.get_text().replace('\xa0', ' '),
                        share=Share.objects.get_or_create(
                            url=wiz.create_or_update_share(docGuid=_['docGuid']).json()['shareUrl']
                        )[0]
                    )
                    tags = _.get('tags').split('*') if _.get('tags') else []
                    doc.tags.clear()
                    doc.tags.add(*tags)
                else:
                    if doc.version != _['version']:
                        doc.created = datetime.fromtimestamp(_['created'] / 1000, tz=get_current_timezone())
                        doc.category = _['category']
                        doc.title = _['title']
                        doc.text = BeautifulSoup(
                            wiz.get_note_view(_['docGuid']).content,
                            features='html.parser'
                        ).body.get_text().replace('\xa0', ' ')
                        doc.share = Share.objects.get_or_create(
                            url=wiz.create_or_update_share(docGuid=_['docGuid']).json()['shareUrl']
                        )[0]
                        doc.save()
                        tags = _.get('tags').split('*') if _.get('tags') else []
                        doc.tags.clear()
                        doc.tags.add(*tags)

        for tag in Tag.objects.all():
            if not tag.doc_set.exists():
                tag.delete()
