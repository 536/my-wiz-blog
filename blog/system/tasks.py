# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/4/5 21:41
# @Author  : https://github.com/536
from celery import shared_task
from django.conf import settings
from wiz import Wiz

from wiznote.models import Tag, Category, Doc


@shared_task
def update_wiz():
    wiz_periodical_update()


def wiz_periodical_update():
    with Wiz(username=settings.WIZ_USERNAME, password=settings.WIZ_PASSWORD) as wiz:
        # tag
        tags = wiz.get_tags().json()['result']
        Tag.objects.periodical_update(tags)

        # category
        categories = wiz.get_category().json()['result']
        Category.objects.periodical_update(categories)

        # doc
        for category in Category.objects.all():
            # TODO: 超过50条时处理
            docs = wiz.get_notes_of_folder(category=category.name,
                                           withAbstract=False,
                                           start=0,
                                           count=50).json()['result']
            Doc.objects.periodical_update(wiz, docs, category)
