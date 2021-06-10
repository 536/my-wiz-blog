# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/6/9 0:57
# @Author  : https://github.com/536
from settings.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
