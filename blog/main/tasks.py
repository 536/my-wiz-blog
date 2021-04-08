# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/4/5 21:41
# @Author  : https://github.com/536
from celery import shared_task

from main.utils import wiz_init


@shared_task
def update_wiz():
    wiz_init()
