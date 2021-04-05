# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/4/5 21:41
# @Author  : https://github.com/536
import logging

from celery import shared_task

from main.utils import wiz_init

logger = logging.getLogger('django')


@shared_task
def update_wiz():
    print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    logger.info('yyyyyyyyyyyyyyyyyyyyyyyyyyyxxxxxxxxxxxxxxxxxxxx')
    wiz_init()
